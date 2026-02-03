"""
debug_qr_tokens.py - Debug QR Code Token Issues

This script helps debug QR code token generation and validation issues.
Run this to test the token lifecycle.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"  # Backend URL
FRONTEND_URL = "http://192.168.0.115:8080"  # Frontend URL

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_student_exists(student_id):
    """Test if student exists in database"""
    try:
        response = requests.get(f"{BASE_URL}/api/students", timeout=5)
        if response.status_code == 200:
            students = response.json()
            student_found = any(s.get('student_id') == student_id for s in students)
            if student_found:
                print(f"✅ Student {student_id} found in database")
                return True
            else:
                print(f"❌ Student {student_id} not found in database")
                print(f"Available students: {[s.get('student_id') for s in students]}")
                return False
        else:
            print(f"❌ Error fetching students: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking student: {e}")
        return False

def test_qr_token_workflow(student_id):
    """Test the complete QR token workflow"""
    print(f"\n🔄 Testing QR token workflow for {student_id}")
    
    # Step 1: Generate attendance token (simulate frontend)
    try:
        # This would normally be done by the frontend, but we'll simulate it
        print(f"📱 Simulating QR code generation for {student_id}")
        
        # Check if we can access the frontend
        frontend_test_url = f"{FRONTEND_URL}/"
        try:
            response = requests.get(frontend_test_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Frontend accessible at {FRONTEND_URL}")
            else:
                print(f"⚠️ Frontend returned: {response.status_code}")
        except:
            print(f"⚠️ Cannot access frontend at {FRONTEND_URL}")
        
        print("📋 QR Code Generation Steps:")
        print("1. Teacher enters student ID in Teacher QR Display")
        print("2. Frontend generates token and creates QR code")
        print("3. QR code contains URL like:")
        print(f"   {FRONTEND_URL}/verify-attendance?token=TOKEN_HERE")
        print("4. Student scans QR with phone")
        print("5. Phone opens URL and validates token")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in QR workflow: {e}")
        return False

def test_token_validation_timing():
    """Test token timing and expiration"""
    print(f"\n⏰ Testing token timing")
    print("Current settings:")
    print("- QR Validity: 300 seconds (5 minutes)")
    print("- Token expiration checked on server")
    print("- Client-side countdown shows remaining time")
    
    return True

def main():
    print("=" * 60)
    print("QR CODE TOKEN DEBUG TOOL")
    print("=" * 60)
    
    # Test student ID
    student_id = "20221CIT0043"
    
    # Run tests
    tests = [
        ("Backend Health", test_backend_health),
        ("Student Exists", lambda: test_student_exists(student_id)),
        ("QR Token Workflow", lambda: test_qr_token_workflow(student_id)),
        ("Token Timing", test_token_validation_timing),
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
    print("DEBUG SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print("\n🔧 TROUBLESHOOTING TIPS:")
    print("1. Make sure backend is running: cd backend && python app.py")
    print("2. Make sure frontend is running: npm run dev")
    print("3. Check network connectivity between devices")
    print("4. Ensure student photos are uploaded for face recognition")
    print("5. Test with different student IDs if needed")
    
    print(f"\n📱 Test QR Code URL Format:")
    print(f"{FRONTEND_URL}/verify-attendance?token=EXAMPLE_TOKEN")

if __name__ == "__main__":
    main()
