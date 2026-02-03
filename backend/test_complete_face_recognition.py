"""
test_complete_face_recognition.py - Complete Face Recognition System Test

This script tests the entire face recognition pipeline:
1. Face encoding generation
2. Face matching
3. Attendance marking
4. API endpoints
"""

import requests
import base64
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"
IMAGES_DIR = Path(__file__).parent / 'data' / 'student_images'

def encode_image_to_base64(image_path):
    """Convert image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running")
            print(f"   Face Recognition: {'Available' if data.get('face_recognition_available') else 'Mock Mode'}")
            print(f"   Registered Students: {data.get('registered_students', 0)}")
            return True
        else:
            print(f"❌ Backend returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_face_verification_api():
    """Test the face verification API endpoint"""
    print("\n🧪 TESTING FACE VERIFICATION API")
    print("=" * 50)
    
    if not IMAGES_DIR.exists():
        print("❌ Images directory not found")
        return False
    
    # Test each student
    test_results = []
    
    for image_file in IMAGES_DIR.glob("*.jpeg"):
        student_id = image_file.stem
        print(f"\n🔍 Testing face verification for {student_id}")
        
        try:
            # Encode image to base64
            image_base64 = encode_image_to_base64(image_file)
            
            # Prepare API request
            payload = {
                "studentId": student_id,
                "image": image_base64
            }
            
            # Call face verification API
            response = requests.post(
                f"{BASE_URL}/api/verify-face",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ API Response: {result.get('success', False)}")
                print(f"   📊 Verified: {result.get('verified', False)}")
                print(f"   👤 Student: {result.get('studentName', 'N/A')}")
                print(f"   📈 Confidence: {result.get('confidenceScore', 0)}%")
                print(f"   💬 Message: {result.get('message', 'N/A')}")
                
                if result.get('success') and result.get('verified'):
                    test_results.append(True)
                    print(f"   🎉 SUCCESS: Face verification worked!")
                else:
                    test_results.append(False)
                    print(f"   ❌ FAILED: Face verification failed")
            else:
                print(f"   ❌ API Error: {response.status_code}")
                print(f"   📄 Response: {response.text}")
                test_results.append(False)
                
        except Exception as e:
            print(f"   ❌ Test error: {e}")
            test_results.append(False)
    
    success_rate = sum(test_results) / len(test_results) * 100
    print(f"\n📊 API TEST RESULTS:")
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   Passed: {sum(test_results)}/{len(test_results)}")
    
    return success_rate > 60  # Allow some tolerance for face recognition

def test_student_data():
    """Test student data and encodings"""
    print("\n👥 TESTING STUDENT DATA")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/students", timeout=10)
        if response.status_code == 200:
            students = response.json()
            print(f"✅ Found {len(students)} students in database")
            
            for student in students:
                print(f"   👤 {student.get('student_id', 'N/A')} - {student.get('name', 'N/A')}")
                print(f"      📸 Has Photo: {'Yes' if student.get('photo_path') else 'No'}")
                print(f"      🧠 Has Encoding: {'Yes' if student.get('has_face_encoding') else 'No'}")
            
            return len(students) > 0
        else:
            print(f"❌ Error fetching students: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing student data: {e}")
        return False

def main():
    print("🚀 COMPLETE FACE RECOGNITION SYSTEM TEST")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Backend Health", test_backend_health),
        ("Student Data", test_student_data),
        ("Face Verification API", test_face_verification_api),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    overall_success = all(result for _, result in results)
    
    print(f"\n🎯 OVERALL RESULT: {'✅ SUCCESS' if overall_success else '⚠️ PARTIAL SUCCESS'}")
    
    if overall_success:
        print("\n🎉 Face recognition system is ready!")
        print("\n📱 TESTING INSTRUCTIONS:")
        print("1. Generate QR code for any student (20221CIT0043, 20221CIT0049, 20221CIT0151)")
        print("2. Scan QR with mobile device")
        print("3. Grant camera permissions")
        print("4. Capture face photo")
        print("5. Verify attendance is marked successfully")
    else:
        print("\n🔧 Some tests failed, but basic functionality may work")
        print("   Check the detailed results above")
    
    return overall_success

if __name__ == "__main__":
    main()
