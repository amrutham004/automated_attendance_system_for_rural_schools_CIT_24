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

packages = ['fastapi', 'uvicorn', 'pydantic', 'cv2', 'PIL', 'numpy']

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

print("\n⚠️  dlib and face-recognition need manual installation")
print("✅ SETUP COMPLETE! (Except face recognition)")
print("Next: Create backend application code")
