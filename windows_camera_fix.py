"""
Windows 11 Camera Permission Fix Guide
Automated Attendance System
"""

def main():
    print("🖥️ WINDOWS 11 CAMERA PERMISSION FIX")
    print("=" * 50)
    print("Solutions for Laptop Camera Access Issues")
    print("=" * 50)
    
    print("\n🔧 QUICK FIXES (Try in Order):")
    
    print("\n1. CHECK WINDOWS CAMERA SETTINGS")
    print("   - Press Windows Key + I")
    print("   - Go to 'Privacy & security'")
    print("   - Click 'Camera' on the left")
    print("   - Enable 'Camera access' (main toggle)")
    print("   - Enable 'Let apps access your camera'")
    print("   - Enable 'Allow desktop apps to access your camera'")
    
    print("\n2. CHECK BROWSER PERMISSIONS")
    print("   - In Chrome/Edge: Click lock icon in address bar")
    print("   - Find 'Camera' in the list")
    print("   - Set to 'Allow'")
    print("   - Refresh the page")
    
    print("\n3. CHECK DEVICE MANAGER")
    print("   - Right-click Start button > Device Manager")
    print("   - Expand 'Cameras' or 'Imaging devices'")
    print("   - Right-click your camera > 'Enable device'")
    print("   - If already enabled, try 'Update driver'")
    
    print("\n4. CHECK WINDOWS SECURITY")
    print("   - Open Windows Security")
    print("   - Go to 'Device security'")
    print("   - Check if camera is being blocked")
    
    print("\n🌐 BROWSER SPECIFIC FIXES:")
    
    print("\nCHROME:")
    print("   - Go to: chrome://settings/content/camera")
    print("   - Ensure 'Sites can ask to use your camera' is selected")
    print("   - Add your site to 'Allow' list if needed")
    
    print("\nEDGE:")
    print("   - Go to: edge://settings/content/camera")
    print("   - Ensure 'Sites can ask to use your camera' is selected")
    print("   - Add your site to 'Allow' list if needed")
    
    print("\n📋 STEP-BY-STEP WALKTHROUGH:")
    print("=" * 40)
    
    steps = [
        "Open Windows Settings (Win + I)",
        "Navigate to Privacy & security",
        "Click on Camera in the left panel",
        "Turn ON 'Camera access' (main toggle)",
        "Turn ON 'Let apps access your camera'",
        "Turn ON 'Allow desktop apps to access your camera'",
        "Open your browser (Chrome/Edge)",
        "Go to your attendance system: http://192.168.0.108:8080",
        "Click the lock icon in address bar",
        "Find Camera in the permissions list",
        "Set Camera permission to 'Allow'",
        "Refresh the page and try camera access"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"{i:2d}. {step}")
    
    print("\n⚠️ COMMON WINDOWS 11 ISSUES:")
    print("- Camera disabled in Privacy settings")
    print("- Browser blocking camera access")
    print("- Camera driver issues")
    print("- Antivirus software blocking camera")
    print("- Windows Security blocking camera")
    
    print("\n🔍 TROUBLESHOOTING STEPS:")
    print("\n1. TEST CAMERA IN WINDOWS CAMERA APP")
    print("   - Open Start menu > Camera app")
    print("   - If camera works here, hardware is OK")
    print("   - If not, it's a driver/hardware issue")
    
    print("\n2. CHECK ANTIVIRUS SETTINGS")
    print("   - Open your antivirus software")
    print("   - Look for camera protection settings")
    print("   - Temporarily disable to test")
    
    print("\n3. RESTART BROWSER")
    print("   - Close all browser windows")
    print("   - Reopen and try again")
    
    print("\n4. TRY DIFFERENT BROWSER")
    print("   - Install Chrome if using Edge")
    print("   - Install Edge if using Chrome")
    print("   - Try Firefox as alternative")
    
    print("\n📞 SYSTEM INFO:")
    print("- Your Network: http://192.168.0.108:8080")
    print("- QR Validity: 1 minute")
    print("- Cut-off Time: 1:00 PM")
    print("- Browser: Chrome/Edge recommended")
    
    print("\n✅ IF STILL NOT WORKING:")
    print("1. Restart your computer")
    print("2. Update Windows 11")
    print("3. Update camera drivers")
    print("4. Run Windows troubleshooter")
    print("   - Settings > System > Troubleshoot")
    
    print("\n🎯 QUICK TEST:")
    print("1. Open: https://webcamtests.com/")
    print("2. Allow camera permissions")
    print("3. See if camera works there")
    print("4. If it works, issue is with your attendance system")
    print("5. If not, issue is with Windows/browser settings")

if __name__ == "__main__":
    main()
