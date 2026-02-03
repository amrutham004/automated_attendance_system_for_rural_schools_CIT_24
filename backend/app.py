"""
FastAPI Face Recognition Backend
Automated Attendance System
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import base64
import json
from datetime import datetime, date
import sqlite3
from pathlib import Path
import uvicorn
import cv2
import numpy as np
from PIL import Image

# Try to import face recognition, but handle gracefully if not available
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
    print("✅ Face recognition library loaded")
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️  Face recognition library not available - using mock mode")

# Initialize FastAPI
app = FastAPI(
    title="Face Recognition Attendance API",
    description="Backend API for automated attendance system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080/", "http://192.168.0.108:8080/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
ENCODINGS_FILE = DATA_DIR / 'face_encodings.json'
STUDENTS_FOLDER = DATA_DIR / 'student_images'
DB_FILE = DATA_DIR / 'attendance.db'

STUDENTS_FOLDER.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Pydantic Models
class StudentPhotoUpload(BaseModel):
    studentId: str
    studentName: str
    image: str
    grade: Optional[str] = None

class FaceVerificationRequest(BaseModel):
    studentId: str
    studentName: str
    image: str

class QRAttendanceWithFace(BaseModel):
    studentId: str
    studentName: str
    image: str

# Database Setup
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            grade TEXT,
            photo_path TEXT,
            has_face_encoding INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            date DATE NOT NULL,
            check_in_time TIME NOT NULL,
            method TEXT DEFAULT 'face_recognition',
            confidence_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            UNIQUE(student_id, date)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def seed_initial_students():
    """Seed the database with initial real students"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Real students to seed
    students = [
        ('20221CIT0043', 'Amrutha M', 'CIT 2022'),
        ('20221CIT0049', 'CM Shalini', 'CIT 2022'),
        ('20221CIT0151', 'Vismaya L', 'CIT 2022')
    ]
    
    for student_id, name, grade in students:
        cursor.execute('''
            INSERT OR IGNORE INTO students (student_id, name, grade)
            VALUES (?, ?, ?)
        ''', (student_id, name, grade))
        print(f"✅ Seeded student: {student_id} - {name}")
    
    conn.commit()
    conn.close()
    print("✅ Initial students seeded successfully")

init_db()
seed_initial_students()

# Face Encoding Functions
def load_encodings():
    if ENCODINGS_FILE.exists():
        with open(ENCODINGS_FILE, 'r') as f:
            data = json.load(f)
            for student_id in data:
                data[student_id]['encoding'] = np.array(data[student_id]['encoding'])
            return data
    return {}

def save_encodings(encodings):
    data = {}
    for student_id, info in encodings.items():
        data[student_id] = {
            'name': info['name'],
            'encoding': info['encoding'].tolist()
        }
    with open(ENCODINGS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

known_encodings = load_encodings()
print(f"✅ Loaded {len(known_encodings)} encodings")

# Helper Functions
def decode_base64_image(image_data: str) -> np.ndarray:
    try:
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Failed to decode image")
        
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Mock face detection for when face_recognition is not available
def mock_face_detection():
    return [(100, 100, 200, 200)]  # Mock face location

def mock_face_encoding(image):
    return np.random.rand(128)  # Mock face encoding

def mock_face_compare(known_encoding, unknown_encoding, tolerance=0.6):
    return [True]  # Always return match for testing

def mock_face_distance(known_encodings, unknown_encoding):
    return [0.3]  # Mock distance

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Face Recognition Attendance API",
        "version": "1.0.0",
        "docs": "/docs",
        "registered_students": len(known_encodings),
        "face_recognition_available": FACE_RECOGNITION_AVAILABLE
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "API is running",
        "timestamp": datetime.now().isoformat(),
        "registered_students": len(known_encodings),
        "face_recognition_available": FACE_RECOGNITION_AVAILABLE
    }

@app.post("/api/admin/upload-student-photo")
async def upload_student_photo(student: StudentPhotoUpload):
    try:
        rgb_image = decode_base64_image(student.image)
        
        if FACE_RECOGNITION_AVAILABLE:
            face_locations = face_recognition.face_locations(rgb_image)
            if len(face_locations) == 0:
                raise HTTPException(status_code=400, detail="No face detected")
            if len(face_locations) > 1:
                raise HTTPException(status_code=400, detail="Multiple faces detected")
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            face_encoding = face_encodings[0]
        else:
            # Mock mode
            face_locations = mock_face_detection()
            face_encoding = mock_face_encoding(rgb_image)
            print("⚠️  Using mock face detection - face_recognition not available")
        
        image_path = STUDENTS_FOLDER / f"{student.studentId}.jpg"
        image_bgr = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(image_path), image_bgr)
        
        known_encodings[student.studentId] = {
            'name': student.studentName,
            'encoding': face_encoding
        }
        save_encodings(known_encodings)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO students 
            (student_id, name, grade, photo_path, has_face_encoding) 
            VALUES (?, ?, ?, ?, 1)
        ''', (student.studentId, student.studentName, student.grade, str(image_path)))
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"Student {student.studentName} registered successfully",
            "studentId": student.studentId,
            "mock_mode": not FACE_RECOGNITION_AVAILABLE
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify-face")
async def verify_face(data: FaceVerificationRequest):
    try:
        image_data = data.image.encode('utf-8') if isinstance(data.image, str) else data.image
        result = recognize_face_from_image(image_data, data.studentId)
        
        if not result["match"]:
            return {
                "success": False,
                "verified": False,
                "message": result.get("message", "Face verification failed"),
                "confidenceScore": 0
            }
        
        current_date = date.today()
        current_time = datetime.now().time()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO attendance 
                (student_id, student_name, date, check_in_time, method, confidence_score)
                VALUES (?, ?, ?, ?, 'face_recognition', ?)
            ''', (result["student_id"], result["student_name"], current_date, current_time, result["confidence"]))
            conn.commit()
            
            return {
                "success": True,
                "verified": True,
                "message": f"Welcome {result['student_name']}! Attendance marked successfully.",
                "confidenceScore": result["confidence"],
                "studentId": result["student_id"],
                "studentName": result["student_name"],
                "timestamp": datetime.now().isoformat(),
                "mock_mode": not FACE_RECOGNITION_AVAILABLE
            }
        except sqlite3.IntegrityError:
            return {
                "success": True,
                "verified": True,
                "message": f"Attendance already marked for {result['student_name']} today.",
                "confidenceScore": result["confidence"],
                "studentId": result["student_id"],
                "studentName": result["student_name"],
                "alreadyMarked": True,
                "mock_mode": not FACE_RECOGNITION_AVAILABLE
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/today-stats")
async def get_today_stats():
    try:
        today = date.today().isoformat()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM students')
        total_students = cursor.fetchone()['count']
        
        cursor.execute(
            'SELECT COUNT(DISTINCT student_id) as count FROM attendance WHERE date = ?',
            (today,)
        )
        present_count = cursor.fetchone()['count']
        
        conn.close()
        
        absent_count = total_students - present_count
        percentage = round((present_count / total_students * 100), 1) if total_students > 0 else 0
        
        return {
            "success": True,
            "percentage": percentage,
            "presentCount": present_count,
            "absentCount": absent_count,
            "totalStudents": total_students,
            "date": today
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/today-list")
async def get_today_attendance_list():
    try:
        today = date.today().isoformat()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, s.grade
            FROM attendance a
            LEFT JOIN students s ON a.student_id = s.student_id
            WHERE a.date = ?
            ORDER BY a.check_in_time DESC
        ''', (today,))
        
        rows = cursor.fetchall()
        conn.close()
        
        attendance_list = []
        for row in rows:
            attendance_list.append({
                "studentId": row['student_id'],
                "studentName": row['student_name'],
                "checkInTime": row['check_in_time'],
                "method": row['method'],
                "confidenceScore": row['confidence_score'],
                "grade": row['grade']
            })
        
        return {
            "success": True,
            "attendance": attendance_list,
            "count": len(attendance_list),
            "date": today
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students")
async def get_all_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        students = []
        for row in rows:
            students.append({
                "id": row['student_id'],
                "name": row['name'],
                "grade": row['grade'],
                "hasFaceEncoding": bool(row['has_face_encoding']),
                "createdAt": row['created_at']
            })
        
        return {
            "success": True,
            "students": students,
            "count": len(students)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/report")
async def get_attendance_report(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    student_id: Optional[str] = Query(None)
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM attendance WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        if student_id:
            query += ' AND student_id = ?'
            params.append(student_id)
        
        query += ' ORDER BY date DESC, check_in_time DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            records.append({
                "studentId": row['student_id'],
                "studentName": row['student_name'],
                "date": row['date'],
                "checkInTime": row['check_in_time'],
                "method": row['method'],
                "confidenceScore": row['confidence_score']
            })
        
        return {
            "success": True,
            "records": records,
            "count": len(records)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Face Recognition Functions
def recognize_face_from_image(image_data: bytes, expected_student_id: str = None) -> dict:
    """
    Recognize face from image data and return match information
    
    Args:
        image_data: Raw image bytes
        expected_student_id: Optional student ID to verify against
    
    Returns:
        dict: Recognition result with match status and details
    """
    try:
        # Decode image
        image = decode_base64_image(image_data)
        
        if FACE_RECOGNITION_AVAILABLE:
            # Real face recognition
            face_locations = face_recognition.face_locations(image, model="hog")
            
            if len(face_locations) == 0:
                return {
                    "match": False,
                    "message": "No face detected in image"
                }
            
            if len(face_locations) > 1:
                return {
                    "match": False,
                    "message": "Multiple faces detected"
                }
            
            # Generate face encoding
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if len(face_encodings) == 0:
                return {
                    "match": False,
                    "message": "Could not generate face encoding"
                }
            
            unknown_encoding = face_encodings[0]
            
            # Load known encodings from database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.student_id, s.name, fe.encoding 
                FROM students s 
                LEFT JOIN face_encodings fe ON s.student_id = fe.student_id 
                WHERE s.has_face_encoding = 1
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return {
                    "match": False,
                    "message": "No registered face encodings found"
                }
            
            # Compare with known encodings
            best_match = None
            best_distance = float('inf')
            
            for row in rows:
                student_id = row['student_id']
                student_name = row['name']
                encoding_bytes = row['encoding']
                
                if encoding_bytes:
                    known_encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
                    
                    # Calculate face distance
                    face_distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
                    
                    if face_distance < best_distance:
                        best_distance = face_distance
                        best_match = {
                            "student_id": student_id,
                            "student_name": student_name,
                            "confidence": max(0, min(100, (1 - face_distance) * 100)),
                            "distance": face_distance
                        }
            
            if best_match and best_distance < 0.6:  # Threshold for face recognition
                # If expected student ID is provided, verify it matches
                if expected_student_id and best_match["student_id"] != expected_student_id:
                    return {
                        "match": False,
                        "message": f"Face does not match expected student {expected_student_id}",
                        "detected_student": best_match["student_name"]
                    }
                
                return {
                    "match": True,
                    "student_id": best_match["student_id"],
                    "student_name": best_match["student_name"],
                    "confidence": round(best_match["confidence"], 2),
                    "distance": round(best_distance, 4)
                }
            else:
                return {
                    "match": False,
                    "message": "No matching face found in database",
                    "best_distance": round(best_distance, 4) if best_match else None
                }
        
        else:
            # Mock mode for testing
            return {
                "match": True,
                "student_id": expected_student_id or "20221CIT0043",
                "student_name": "Test Student",
                "confidence": 95.0,
                "message": "Mock mode - face recognition not available"
            }
    
    except Exception as e:
        return {
            "match": False,
            "message": f"Face recognition error: {str(e)}"
        }

# Startup
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 FastAPI Face Recognition Backend")
    print("=" * 70)
    print(f"📁 Data: {DATA_DIR}")
    print(f"🖼️  Images: {STUDENTS_FOLDER}")
    print(f"👥 Students: {len(known_encodings)}")
    print(f"📚 Docs: http://localhost:8000/docs or http://192.168.0.108:8000/docs")
    print(f"🔧 Face Recognition: {'Available' if FACE_RECOGNITION_AVAILABLE else 'Mock Mode'}")
    print("=" * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
