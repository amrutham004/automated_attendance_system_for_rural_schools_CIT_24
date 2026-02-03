# Complete Face Recognition Backend Setup Guide
**For Automated Attendance System**

---

## 📖 Table of Contents
1. [Installation & Environment Setup](#part-1-installation--environment-setup)
2. [Backend Code Setup](#part-2-backend-code-setup)
3. [Testing & Verification](#part-3-testing--verification)
4. [Troubleshooting](#part-4-troubleshooting)

---

# PART 1: Installation & Environment Setup

## Prerequisites Check
- Python 3.8 or higher
- pip (Python package manager)
- Git
- 4GB+ RAM
- Webcam (for testing)

## Step 1: Verify Python Installation

### Windows:
```bash
python --version
# Should show: Python 3.8.x or higher
# If not installed: https://www.python.org/downloads/
# ⚠️ CHECK "Add Python to PATH" during installation
```

### macOS:
```bash
python3 --version
# If not installed:
brew install python@3.11
```

### Linux (Ubuntu/Debian):
```bash
python3 --version
# If not installed:
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

## Step 2: Navigate to Project

```bash
cd path/to/automated-attendance-system
# Verify: you should see src/, public/, package.json
```

## Step 3: Create Backend Directory

```bash
mkdir backend
cd backend
pwd  # Verify location
```

## Step 4: Create Virtual Environment

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
# You should see (venv) in prompt
```

### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
# You should see (venv) in prompt
```

### Verification:
```bash
which python    # macOS/Linux
where python    # Windows
# Should show path inside venv folder
```

## Step 5: Upgrade pip

```bash
pip install --upgrade pip
pip --version
# Should show pip 23.x or higher
```

## Step 6: Install CMake

### Windows:
```bash
# Option A: Using pip
pip install cmake

# Option B: Download installer
# https://cmake.org/download/
# Check "Add CMake to PATH"

# Option C: Visual Studio Build Tools
# https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++"
```

### macOS:
```bash
brew install cmake
cmake --version
```

### Linux:
```bash
sudo apt update
sudo apt install cmake build-essential
cmake --version
```

## Step 7: System Dependencies (Linux Only)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev

# Fedora/RHEL
sudo dnf install \
    gcc gcc-c++ cmake \
    python3-devel \
    openblas-devel \
    lapack-devel
```

## Step 8: Create requirements.txt

Create file `requirements.txt`:

```text
# FastAPI and server
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Data validation
pydantic==2.5.3

# Face recognition
face-recognition==1.3.0
dlib==19.24.2

# Image processing
opencv-python==4.8.1.78
Pillow==10.1.0
numpy==1.24.3
```

## Step 9: Install Dependencies

```bash
# This takes 5-10 minutes
pip install -r requirements.txt
```

### If dlib fails (Windows):

```bash
# Method 1: Pre-compiled wheel
# Download from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x
# Then:
pip install dlib-19.24.2-cp311-cp311-win_amd64.whl
pip install face-recognition

# Method 2: Using conda
conda install -c conda-forge dlib
pip install face-recognition
```

### If dlib fails (macOS):

```bash
brew install cmake boost boost-python3
pip install dlib
pip install face-recognition
```

### If dlib fails (Linux):

```bash
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev
pip install dlib
pip install face-recognition
```

## Step 10: Verify Installation

Create `test_imports.py`:

```python
import face_recognition
import cv2
import fastapi
import numpy as np
from PIL import Image

print("✅ All imports successful!")
print("face_recognition version:", face_recognition.__version__)
print("OpenCV version:", cv2.__version__)
print("FastAPI version:", fastapi.__version__)
```

Run:
```bash
python test_imports.py
```

## Step 11: Create Project Structure

```bash
# Windows:
mkdir data
mkdir data\student_images

# macOS/Linux:
mkdir -p data/student_images
```

### Verify structure:
```
backend/
├── venv/
├── data/
│   └── student_images/
├── requirements.txt
└── test_imports.py
```

## Step 12: Create .gitignore

Create `.gitignore`:

```text
# Virtual Environment
venv/
env/
.venv/

# Data files
data/
*.db
*.json

# Python
__pycache__/
*.py[cod]
*$py.class

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

## Step 13: System Check

Create `system_check.py`:

```python
import sys
import platform

print("=" * 60)
print("SYSTEM INFORMATION")
print("=" * 60)
print(f"Python Version: {sys.version}")
print(f"Platform: {platform.platform()}")
print()

print("CHECKING PACKAGES")
print("=" * 60)

packages = ['fastapi', 'uvicorn', 'pydantic', 'face_recognition', 'cv2', 'PIL', 'numpy']

for package in packages:
    try:
        if package == 'cv2':
            __import__('cv2')
            print(f"✅ opencv-python")
        elif package == 'PIL':
            __import__('PIL')
            print(f"✅ Pillow")
        else:
            __import__(package)
            print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - NOT INSTALLED")

print("\n✅ SETUP COMPLETE!")
print("Next: Create backend application code")
```

Run:
```bash
python system_check.py
```

---

# PART 2: Backend Code Setup

## Step 1: Create Environment File

Create `.env`:

```text
# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=True

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Face Recognition
FACE_RECOGNITION_TOLERANCE=0.6
MIN_CONFIDENCE_SCORE=40

# Paths
DB_PATH=data/attendance.db
ENCODINGS_FILE=data/face_encodings.json
IMAGES_FOLDER=data/student_images
```

## Step 2: Create app.py

Create `app.py` with this complete code:

```python
"""
FastAPI Face Recognition Backend
Automated Attendance System
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import face_recognition
import cv2
import numpy as np
import base64
import json
from datetime import datetime, date
import sqlite3
from pathlib import Path
import uvicorn

# Initialize FastAPI
app = FastAPI(
    title="Face Recognition Attendance API",
    description="Backend API for automated attendance system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

init_db()

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

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Face Recognition Attendance API",
        "version": "1.0.0",
        "docs": "/docs",
        "registered_students": len(known_encodings)
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "API is running",
        "timestamp": datetime.now().isoformat(),
        "registered_students": len(known_encodings)
    }

@app.post("/api/admin/upload-student-photo")
async def upload_student_photo(student: StudentPhotoUpload):
    try:
        rgb_image = decode_base64_image(student.image)
        face_locations = face_recognition.face_locations(rgb_image)
        
        if len(face_locations) == 0:
            raise HTTPException(status_code=400, detail="No face detected")
        
        if len(face_locations) > 1:
            raise HTTPException(status_code=400, detail="Multiple faces detected")
        
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        face_encoding = face_encodings[0]
        
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
            "studentId": student.studentId
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify-face")
async def verify_face(data: FaceVerificationRequest):
    try:
        if data.studentId not in known_encodings:
            return {
                "success": False,
                "verified": False,
                "message": "No reference photo found",
                "confidenceScore": 0
            }
        
        rgb_image = decode_base64_image(data.image)
        face_locations = face_recognition.face_locations(rgb_image)
        
        if len(face_locations) == 0:
            return {
                "success": False,
                "verified": False,
                "message": "No face detected",
                "confidenceScore": 0
            }
        
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        captured_encoding = face_encodings[0]
        
        stored_encoding = known_encodings[data.studentId]['encoding']
        matches = face_recognition.compare_faces([stored_encoding], captured_encoding, tolerance=0.6)
        face_distance = face_recognition.face_distance([stored_encoding], captured_encoding)[0]
        
        confidence_score = max(0, min(100, (1 - face_distance) * 100))
        
        if matches[0] and confidence_score >= 40:
            current_date = date.today()
            current_time = datetime.now().time()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO attendance 
                    (student_id, student_name, date, check_in_time, method, confidence_score)
                    VALUES (?, ?, ?, ?, 'face_recognition', ?)
                ''', (data.studentId, data.studentName, current_date, current_time, confidence_score))
                conn.commit()
                
                return {
                    "success": True,
                    "verified": True,
                    "message": f"Welcome {data.studentName}! Attendance marked.",
                    "confidenceScore": round(confidence_score, 2),
                    "timestamp": datetime.now().isoformat()
                }
            except sqlite3.IntegrityError:
                return {
                    "success": True,
                    "verified": True,
                    "message": f"Already marked attendance today.",
                    "confidenceScore": round(confidence_score, 2),
                    "alreadyMarked": True
                }
            finally:
                conn.close()
        else:
            return {
                "success": False,
                "verified": False,
                "message": "Face verification failed",
                "confidenceScore": round(confidence_score, 2)
            }
            
    except HTTPException:
        raise
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

# Startup
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 FastAPI Face Recognition Backend")
    print("=" * 70)
    print(f"📁 Data: {DATA_DIR}")
    print(f"🖼️  Images: {STUDENTS_FOLDER}")
    print(f"👥 Students: {len(known_encodings)}")
    print(f"📚 Docs: http://localhost:8000/docs")
    print("=" * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

## Step 3: Test the Backend

```bash
python app.py
```

### Expected Output:
```
======================================================================
🚀 FastAPI Face Recognition Backend
======================================================================
📁 Data: /path/to/backend/data
🖼️  Images: /path/to/backend/data/student_images
👥 Students: 0
📚 Docs: http://localhost:8000/docs
======================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Database initialized
✅ Loaded 0 encodings
INFO:     Application startup complete.
```

## Step 4: Test API

Open browser: `http://localhost:8000/docs`

Test health endpoint: `http://localhost:8000/api/health`

---

# PART 3: Testing & Verification

## Create Test Script

Create `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("TESTING API")
print("=" * 60)

# Test 1: Health
response = requests.get(f"{BASE_URL}/api/health")
if response.status_code == 200:
    print("✅ Health check passed")
else:
    print("❌ Health check failed")

# Test 2: Stats
response = requests.get(f"{BASE_URL}/api/attendance/today-stats")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Stats: {data['totalStudents']} students, {data['presentCount']} present")
else:
    print("❌ Stats failed")

# Test 3: Students
response = requests.get(f"{BASE_URL}/api/students")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Students: {data['count']} registered")
else:
    print("❌ Students endpoint failed")

print("\n✅ TESTING COMPLETE")
```

Run:
```bash
python test_api.py
```

## Upload Test Student

Create `test_upload.py`:

```python
import requests
import base64

BASE_URL = "http://localhost:8000"

def upload_student(student_id, name, image_path, grade="10th"):
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    payload = {
        "studentId": student_id,
        "studentName": name,
        "image": f"data:image/jpeg;base64,{image_base64}",
        "grade": grade
    }
    
    response = requests.post(
        f"{BASE_URL}/api/admin/upload-student-photo",
        json=payload
    )
    
    if response.status_code == 200:
        print(f"✅ Uploaded {name}")
        return True
    else:
        print(f"❌ Failed: {response.json()}")
        return False

# Upload test student
# Replace with actual image path
upload_student("STU001", "John Doe", "test.jpg", "10th")
```

---

# PART 4: Troubleshooting

## Quick Diagnostic

Create `quick_diagnostic.py`:

```python
import sys
import os

print("=" * 60)
print("DIAGNOSTIC CHECK")
print("=" * 60)

# Python version
print(f"\nPython: {sys.version}")
if sys.version_info >= (3, 8):
    print("✅ Version OK")
else:
    print("❌ Need Python 3.8+")

# Virtual environment
venv_active = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
)
print(f"\nVirtual Env: {'✅ Active' if venv_active else '❌ Not Active'}")

# Packages
packages = ['fastapi', 'face_recognition', 'cv2', 'PIL', 'numpy']
print("\nPackages:")
for pkg in packages:
    try:
        if pkg == 'cv2':
            __import__('cv2')
        else:
            __import__(pkg)
        print(f"  ✅ {pkg}")
    except ImportError:
        print(f"  ❌ {pkg}")

# Directories
print("\nDirectories:")
for d in ['data', 'data/student_images']:
    print(f"  {'✅' if os.path.exists(d) else '❌'} {d}")

# Files
print("\nFiles:")
for f in ['app.py', 'requirements.txt']:
    print(f"  {'✅' if os.path.exists(f) else '❌'} {f}")

print("\n" + "=" * 60)
```

## Common Issues

### Issue: dlib won't install

**Windows:**
```bash
# Use pre-compiled wheel
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.2-cp311-cp311-win_amd64.whl
```

**macOS:**
```bash
brew install cmake boost
pip install dlib
```

**Linux:**
```bash
sudo apt-get install cmake build-essential
pip install dlib
```

### Issue: Port in use

```bash
# Find process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in app.py:
uvicorn.run(app, port=8001)
```

### Issue: CORS errors

Check `app.py` has:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: No face detected

- Use good lighting
- Face directly facing camera
- Clear, high-resolution image
- No glasses/masks

### Issue: Low confidence scores

Adjust tolerance in `app.py`:
```python
# Line in verify_face function
matches = face_recognition.compare_faces(
    [stored_encoding], 
    captured_encoding, 
    tolerance=0.7  # Increase for more lenient
)
```

---

## Final Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] `app.py` created
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Health endpoint works
- [ ] Database created
- [ ] Can upload student photos
- [ ] Face recognition works

---

## Next Steps

1. **Test with real photos**
2. **Integrate with frontend**
3. **Deploy to production**

---

## Support

For issues:
1. Run `quick_diagnostic.py`
2. Check error messages
3. Review troubleshooting section
4. Check logs in terminal

**You're ready to go!** 🚀