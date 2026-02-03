"""
test_upload_real_students.py - Test Photo Upload for Real Students

This script tests uploading student photos to the backend API.
Run this after adding actual student photos to the test_photos folder.

Requirements:
- Backend server running on http://localhost:8000
- Student photos in test_photos folder:
  - 20221CIT0043_amrutha.jpg
  - 20221CIT0049_shalini.jpg
  - 20221CIT0151_vismaya.jpg
"""

import requests
import base64
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

# Real student data
students = [
    ("20221CIT0043", "Amrutha M", "20221CIT0043_amrutha.jpg"),
    ("20221CIT0049", "CM Shalini", "20221CIT0049_shalini.jpg"),
    ("20221CIT0151", "Vismaya L", "20221CIT0151_vismaya.jpg"),
]

def test_student_photo_upload():
    """Test uploading photos for all real students"""
    
    print("=" * 60)
    print("TESTING STUDENT PHOTO UPLOAD")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server not responding correctly")
            return False
        print("✅ Backend server is running")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend server first:")
        print("cd backend && python app.py")
        return False
    
    success_count = 0
    total_count = len(students)
    
    for student_id, name, photo_filename in students:
        print(f"\n📸 Processing: {name} ({student_id})")
        
        # Check if photo file exists
        photo_path = Path("test_photos") / photo_filename
        if not photo_path.exists():
            print(f"⚠️  Photo file not found: {photo_path}")
            print("   Add student photos to test_photos folder and try again")
            continue
        
        try:
            # Read and encode image
            with open(photo_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode()
            
            # Prepare payload
            payload = {
                "studentId": student_id,
                "studentName": name,
                "image": f"data:image/jpeg;base64,{image_base64}",
                "grade": "CIT 2022"
            }
            
            # Upload photo
            response = requests.post(
                f"{BASE_URL}/api/admin/upload-student-photo",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result.get('message', 'Photo uploaded')}")
                success_count += 1
            else:
                print(f"❌ Failed: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Response: {response.text}")
        
        except Exception as e:
            print(f"❌ Error processing {name}: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"UPLOAD SUMMARY: {success_count}/{total_count} successful")
    print("=" * 60)
    
    if success_count == total_count:
        print("🎉 All student photos uploaded successfully!")
        print("\nNext steps:")
        print("1. Test face recognition with real student IDs")
        print("2. Generate QR codes using real student IDs")
        print("3. Test complete attendance workflow")
    else:
        print("⚠️  Some uploads failed. Check the errors above.")
    
    return success_count == total_count

def test_face_recognition_availability():
    """Test if face recognition is available on the backend"""
    
    print("\n🔍 CHECKING FACE RECOGNITION STATUS...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            face_recognition_status = health_data.get('face_recognition_available', False)
            
            if face_recognition_status:
                print("✅ Face recognition is available")
                return True
            else:
                print("⚠️  Face recognition not available (running in mock mode)")
                print("   Photos uploaded but face verification will use mock responses")
                return False
        else:
            print("❌ Could not check face recognition status")
            return False
    
    except Exception as e:
        print(f"❌ Error checking face recognition: {e}")
        return False

if __name__ == "__main__":
    print("📋 Student Photo Upload Test")
    print("This will upload photos for:")
    for student_id, name, _ in students:
        print(f"   - {name} ({student_id})")
    
    input("\nPress Enter to continue...")
    
    # Test face recognition availability first
    face_recognition_available = test_face_recognition_availability()
    
    # Test photo uploads
    upload_success = test_student_photo_upload()
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Face Recognition: {'✅ Available' if face_recognition_available else '⚠️  Mock Mode'}")
    print(f"Photo Uploads: {'✅ Success' if upload_success else '❌ Failed'}")
    
    if upload_success:
        print("\n🚀 Ready for testing:")
        print("1. Go to Teacher QR Display")
        print("2. Enter: 20221CIT0043")
        print("3. Generate QR code and test")
        print("4. Try face recognition with real student IDs")
