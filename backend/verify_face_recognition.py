"""
Face Recognition Backend Verification Script
Tests real face detection, encoding, and comparison
"""

import sys
import os
import requests
import base64
import json
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_RESULTS = []

def log_test(test_name, status, details=""):
    """Log test result"""
    result = {
        "test": test_name,
        "status": status,
        "details": details
    }
    TEST_RESULTS.append(result)
    
    status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{status_icon} {test_name}")
    if details:
        print(f"   {details}")

def check_server_status():
    """Check if server is running and face recognition availability"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('face_recognition_available') == True:
                log_test("Server Health Check", "PASS", "Face recognition available")
                return True
            else:
                log_test("Server Health Check", "FAIL", "Face recognition NOT available - still in mock mode")
                return False
        else:
            log_test("Server Health Check", "FAIL", f"Server returned {response.status_code}")
            return False
    except Exception as e:
        log_test("Server Health Check", "FAIL", f"Cannot connect to server: {str(e)}")
        return False

def create_test_image_base64():
    """Create a simple test image (1x1 pixel) for testing"""
    # This creates a minimal 1x1 red pixel image
    import io
    from PIL import Image
    
    # Create a simple test image (100x100 with a face-like pattern)
    img = Image.new('RGB', (100, 100), color='white')
    
    # Add some face-like features (simplified)
    pixels = img.load()
    # Add eyes
    for i in range(30, 40):
        for j in range(30, 40):
            pixels[i, j] = (0, 0, 0)  # Black
    for i in range(60, 70):
        for j in range(30, 40):
            pixels[i, j] = (0, 0, 0)  # Black
    # Add mouth
    for i in range(30, 70):
        pixels[i, 60] = (255, 0, 0)  # Red
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def test_student_photo_upload():
    """Test uploading a student photo"""
    try:
        test_image = create_test_image_base64()
        
        payload = {
            "studentId": "TEST001",
            "studentName": "Test Student",
            "image": test_image,
            "grade": "10th"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/admin/upload-student-photo",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('mock_mode') == True:
                log_test("Student Photo Upload", "FAIL", "Still using mock mode")
                return False
            else:
                log_test("Student Photo Upload", "PASS", f"Uploaded: {data.get('message')}")
                return True
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            log_test("Student Photo Upload", "FAIL", f"Upload failed: {error_detail}")
            return False
            
    except Exception as e:
        log_test("Student Photo Upload", "FAIL", f"Exception: {str(e)}")
        return False

def test_face_verification():
    """Test face verification with uploaded student"""
    try:
        test_image = create_test_image_base64()
        
        payload = {
            "studentId": "TEST001",
            "studentName": "Test Student",
            "image": test_image
        }
        
        response = requests.post(
            f"{BASE_URL}/api/verify-face",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('mock_mode') == True:
                log_test("Face Verification", "FAIL", "Still using mock mode")
                return False
            
            confidence = data.get('confidenceScore', 0)
            verified = data.get('verified', False)
            
            if verified and confidence > 0:
                log_test("Face Verification", "PASS", f"Verified with {confidence}% confidence")
                return True
            else:
                log_test("Face Verification", "FAIL", f"Verification failed: {data.get('message')}")
                return False
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            log_test("Face Verification", "FAIL", f"Verification failed: {error_detail}")
            return False
            
    except Exception as e:
        log_test("Face Verification", "FAIL", f"Exception: {str(e)}")
        return False

def test_multiple_faces_detection():
    """Test detection of multiple faces in an image"""
    try:
        # Create an image that should ideally have one face
        test_image = create_test_image_base64()
        
        payload = {
            "studentId": "TEST002",
            "studentName": "Multi Face Test",
            "image": test_image,
            "grade": "11th"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/admin/upload-student-photo",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('mock_mode') == True:
                log_test("Multiple Faces Detection", "FAIL", "Still using mock mode")
                return False
            else:
                log_test("Multiple Faces Detection", "PASS", "Face detection working")
                return True
        elif response.status_code == 400:
            error_detail = response.json().get('detail', '')
            if 'No face detected' in error_detail:
                log_test("Multiple Faces Detection", "PASS", "Properly detected no faces in test image")
                return True
            elif 'Multiple faces detected' in error_detail:
                log_test("Multiple Faces Detection", "PASS", "Properly detected multiple faces")
                return True
            else:
                log_test("Multiple Faces Detection", "FAIL", f"Unexpected error: {error_detail}")
                return False
        else:
            log_test("Multiple Faces Detection", "FAIL", f"Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        log_test("Multiple Faces Detection", "FAIL", f"Exception: {str(e)}")
        return False

def test_confidence_score_realism():
    """Test if confidence scores are realistic (not always 100%)"""
    try:
        # Test with different images to get varying confidence scores
        confidences = []
        
        for i in range(3):
            test_image = create_test_image_base64()
            
            payload = {
                "studentId": "TEST001",
                "studentName": "Test Student",
                "image": test_image
            }
            
            response = requests.post(
                f"{BASE_URL}/api/verify-face",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get('mock_mode', True):
                    confidence = data.get('confidenceScore', 0)
                    confidences.append(confidence)
                    time.sleep(0.5)  # Small delay between requests
        
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            # Real face recognition should have varying scores, not always 100%
            if 40 <= avg_confidence <= 95:
                log_test("Confidence Score Realism", "PASS", f"Realistic scores: {confidences}")
                return True
            else:
                log_test("Confidence Score Realism", "FAIL", f"Unrealistic scores: {confidences}")
                return False
        else:
            log_test("Confidence Score Realism", "FAIL", "No valid confidence scores collected")
            return False
            
    except Exception as e:
        log_test("Confidence Score Realism", "FAIL", f"Exception: {str(e)}")
        return False

def test_database_operations():
    """Test database operations are working"""
    try:
        # Check if student was saved to database
        response = requests.get(f"{BASE_URL}/api/students", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            students = data.get('students', [])
            
            # Check if our test student exists
            test_student = None
            for student in students:
                if student.get('id') == 'TEST001':
                    test_student = student
                    break
            
            if test_student and test_student.get('hasFaceEncoding'):
                log_test("Database Operations", "PASS", f"Student saved with face encoding: {test_student}")
                return True
            elif test_student:
                log_test("Database Operations", "FAIL", "Student saved but no face encoding")
                return False
            else:
                log_test("Database Operations", "FAIL", "Test student not found in database")
                return False
        else:
            log_test("Database Operations", "FAIL", f"Failed to get students: {response.status_code}")
            return False
            
    except Exception as e:
        log_test("Database Operations", "FAIL", f"Exception: {str(e)}")
        return False

def test_attendance_workflow():
    """Test complete attendance workflow"""
    try:
        # Get today's attendance stats
        response = requests.get(f"{BASE_URL}/api/attendance/today-stats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('presentCount', 0) > 0:
                log_test("Attendance Workflow", "PASS", f"Attendance recorded: {data.get('presentCount')} present")
                return True
            else:
                log_test("Attendance Workflow", "FAIL", "No attendance recorded")
                return False
        else:
            log_test("Attendance Workflow", "FAIL", f"Failed to get stats: {response.status_code}")
            return False
            
    except Exception as e:
        log_test("Attendance Workflow", "FAIL", f"Exception: {str(e)}")
        return False

def check_face_recognition_imports():
    """Check if face recognition libraries are properly imported"""
    try:
        # Test imports directly
        import face_recognition
        import dlib
        
        # Check versions
        fr_version = getattr(face_recognition, '__version__', 'unknown')
        
        log_test("Face Recognition Imports", "PASS", f"face_recognition v{fr_version}, dlib available")
        return True
        
    except ImportError as e:
        log_test("Face Recognition Imports", "FAIL", f"Import error: {str(e)}")
        return False

def generate_report():
    """Generate final report"""
    print("\n" + "="*70)
    print("🎯 FACE RECOGNITION BACKEND VERIFICATION REPORT")
    print("="*70)
    
    passed = sum(1 for test in TEST_RESULTS if test['status'] == 'PASS')
    failed = sum(1 for test in TEST_RESULTS if test['status'] == 'FAIL')
    warnings = sum(1 for test in TEST_RESULTS if test['status'] == 'WARNING')
    total = len(TEST_RESULTS)
    
    print(f"\n📊 SUMMARY: {passed} PASSED, {failed} FAILED, {warnings} WARNINGS out of {total} tests")
    
    print("\n📋 DETAILED RESULTS:")
    for test in TEST_RESULTS:
        status_icon = "✅" if test['status'] == 'PASS' else "❌" if test['status'] == 'FAIL' else "⚠️"
        print(f"{status_icon} {test['test']}")
        if test['details']:
            print(f"   {test['details']}")
    
    print("\n" + "="*70)
    if failed == 0 and warnings == 0:
        print("🎉 ALL TESTS PASSED! Face recognition is working correctly!")
        print("✅ Your backend is ready for production use!")
    elif failed == 0:
        print("⚠️  ALL CRITICAL TESTS PASSED! Minor warnings present.")
        print("✅ Your backend is functional with some limitations.")
    else:
        print("❌ SOME TESTS FAILED! Face recognition needs attention.")
        print("🔧 Please check the failed tests above.")
    
    print("="*70)
    
    return failed == 0

def main():
    """Main test execution"""
    print("🔍 Starting Face Recognition Backend Verification...")
    print("Testing REAL face detection (not mock mode)...\n")
    
    # Run all tests
    tests = [
        check_server_status,
        check_face_recognition_imports,
        test_student_photo_upload,
        test_face_verification,
        test_multiple_faces_detection,
        test_confidence_score_realism,
        test_database_operations,
        test_attendance_workflow
    ]
    
    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            log_test(test_func.__name__, "FAIL", f"Test crashed: {str(e)}")
        print()
    
    # Generate final report
    success = generate_report()
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
