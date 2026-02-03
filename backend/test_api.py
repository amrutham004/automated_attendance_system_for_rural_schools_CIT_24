import requests
import time

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("TESTING API")
print("=" * 60)

# Wait a moment for server to be ready
time.sleep(2)

# Test 1: Health
try:
    response = requests.get(f"{BASE_URL}/api/health")
    if response.status_code == 200:
        data = response.json()
        print("✅ Health check passed")
        print(f"   Status: {data['status']}")
        print(f"   Face Recognition Available: {data['face_recognition_available']}")
    else:
        print("❌ Health check failed")
except Exception as e:
    print(f"❌ Health check error: {e}")

# Test 2: Root
try:
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print("✅ Root endpoint passed")
        print(f"   Message: {data['message']}")
        print(f"   Registered Students: {data['registered_students']}")
    else:
        print("❌ Root endpoint failed")
except Exception as e:
    print(f"❌ Root endpoint error: {e}")

# Test 3: Stats
try:
    response = requests.get(f"{BASE_URL}/api/attendance/today-stats")
    if response.status_code == 200:
        data = response.json()
        print("✅ Stats endpoint passed")
        print(f"   Total Students: {data['totalStudents']}")
        print(f"   Present: {data['presentCount']}")
    else:
        print("❌ Stats endpoint failed")
except Exception as e:
    print(f"❌ Stats endpoint error: {e}")

# Test 4: Students
try:
    response = requests.get(f"{BASE_URL}/api/students")
    if response.status_code == 200:
        data = response.json()
        print("✅ Students endpoint passed")
        print(f"   Students registered: {data['count']}")
    else:
        print("❌ Students endpoint failed")
except Exception as e:
    print(f"❌ Students endpoint error: {e}")

print("\n✅ BASIC API TESTING COMPLETE!")
print("📚 API Documentation: http://localhost:8000/docs")
print("🔧 Face Recognition: Mock Mode (dlib not installed)")
