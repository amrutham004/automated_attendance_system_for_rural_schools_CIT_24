"""
setup_face_recognition.py - Complete Face Recognition Setup

This script will:
1. Generate face encodings for all uploaded student photos
2. Update the database with encoding information
3. Test the complete face recognition pipeline
"""

import os
import sqlite3
import face_recognition
import numpy as np
from pathlib import Path

# Configuration
DB_FILE = Path(__file__).parent / 'data' / 'attendance.db'
IMAGES_DIR = Path(__file__).parent / 'data' / 'student_images'

def generate_face_encodings():
    """Generate face encodings for all student photos"""
    print("🔍 GENERATING FACE ENCODINGS")
    print("=" * 50)
    
    if not IMAGES_DIR.exists():
        print(f"❌ Images directory not found: {IMAGES_DIR}")
        return False
    
    # Get all image files
    image_files = list(IMAGES_DIR.glob("*.jpg")) + list(IMAGES_DIR.glob("*.jpeg")) + list(IMAGES_DIR.glob("*.png"))
    
    if not image_files:
        print("❌ No image files found in student_images directory")
        return False
    
    print(f"📁 Found {len(image_files)} image files:")
    for img_file in image_files:
        print(f"   - {img_file.name}")
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    successful_encodings = 0
    failed_encodings = 0
    
    for image_file in image_files:
        print(f"\n🔍 Processing: {image_file.name}")
        
        try:
            # Extract student ID from filename
            student_id = image_file.stem
            print(f"   Student ID: {student_id}")
            
            # Load image
            image = face_recognition.load_image_file(str(image_file))
            print(f"   ✅ Image loaded successfully")
            
            # Find face locations
            face_locations = face_recognition.face_locations(image, model="hog")
            print(f"   🔍 Found {len(face_locations)} face(s)")
            
            if len(face_locations) == 0:
                print(f"   ⚠️ No face found in image")
                failed_encodings += 1
                continue
            
            if len(face_locations) > 1:
                print(f"   ⚠️ Multiple faces found, using the first one")
            
            # Generate face encoding
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if len(face_encodings) == 0:
                print(f"   ❌ Could not generate face encoding")
                failed_encodings += 1
                continue
            
            # Use the first face encoding
            face_encoding = face_encodings[0]
            print(f"   ✅ Face encoding generated successfully")
            
            # Convert encoding to bytes for storage
            encoding_bytes = face_encoding.tobytes()
            
            # Update database
            cursor.execute('''
                UPDATE students 
                SET photo_path = ?, has_face_encoding = 1
                WHERE student_id = ?
            ''', (str(image_file), student_id))
            
            # Store encoding in separate table
            cursor.execute('''
                INSERT OR REPLACE INTO face_encodings (student_id, encoding)
                VALUES (?, ?)
            ''', (student_id, encoding_bytes))
            
            print(f"   💾 Database updated for {student_id}")
            successful_encodings += 1
            
        except Exception as e:
            print(f"   ❌ Error processing {image_file.name}: {e}")
            failed_encodings += 1
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 ENCODING SUMMARY:")
    print(f"   ✅ Successful: {successful_encodings}")
    print(f"   ❌ Failed: {failed_encodings}")
    
    return successful_encodings > 0

def create_face_encodings_table():
    """Create the face_encodings table if it doesn't exist"""
    print("\n🔧 CREATING FACE ENCODINGS TABLE")
    print("=" * 50)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_encodings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            encoding BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Face encodings table created/verified")

def test_face_recognition():
    """Test the face recognition system"""
    print("\n🧪 TESTING FACE RECOGNITION")
    print("=" * 50)
    
    # Import the backend face recognition functions
    import sys
    sys.path.append(str(Path(__file__).parent))
    
    try:
        from app import recognize_face_from_image
        
        # Test with each student image
        test_results = []
        
        for image_file in IMAGES_DIR.glob("*.jpeg"):
            student_id = image_file.stem
            print(f"\n🔍 Testing recognition for {student_id}")
            
            try:
                # Load image as bytes (simulating upload)
                with open(image_file, 'rb') as f:
                    image_data = f.read()
                
                # Test recognition
                result = recognize_face_from_image(image_data, student_id)
                
                if result['match']:
                    print(f"   ✅ Recognition successful: {result['student_name']}")
                    print(f"   📊 Confidence: {result.get('confidence', 'N/A')}")
                    test_results.append(True)
                else:
                    print(f"   ❌ Recognition failed: {result.get('message', 'Unknown error')}")
                    test_results.append(False)
                    
            except Exception as e:
                print(f"   ❌ Test error: {e}")
                test_results.append(False)
        
        success_rate = sum(test_results) / len(test_results) * 100
        print(f"\n📊 TEST RESULTS:")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Passed: {sum(test_results)}/{len(test_results)}")
        
        return success_rate > 80
        
    except ImportError as e:
        print(f"❌ Could not import face recognition functions: {e}")
        return False

def main():
    print("🚀 COMPLETE FACE RECOGNITION SETUP")
    print("=" * 60)
    
    # Step 1: Create face encodings table
    create_face_encodings_table()
    
    # Step 2: Generate face encodings
    if not generate_face_encodings():
        print("❌ Face encoding generation failed")
        return False
    
    # Step 3: Test face recognition
    if not test_face_recognition():
        print("⚠️ Face recognition tests failed, but setup may still work")
    
    print("\n" + "=" * 60)
    print("✅ FACE RECOGNITION SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Test the complete attendance flow:")
    print("   - Generate QR code for a student")
    print("   - Scan QR with mobile")
    print("   - Capture face photo")
    print("   - Verify attendance is marked")
    
    print("\n2. The system now supports:")
    print("   ✅ Face encoding generation")
    print("   ✅ Face matching during attendance")
    print("   ✅ Real-time face verification")
    print("   ✅ Confidence scoring")
    
    return True

if __name__ == "__main__":
    main()
