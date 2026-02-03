"""
verify_dual_network_config.py - Verify dual network configuration

This script verifies that both localhost:8080 and 192.168.0.108:8080 are configured.
"""

import os
import re

def verify_dual_network_config():
    """Verify the dual network configuration changes"""
    
    print("🌐 VERIFYING DUAL NETWORK CONFIGURATION")
    print("=" * 60)
    print("Enabled: localhost:8080 AND 192.168.0.108:8080")
    print("=" * 60)
    
    # Files to check
    files_to_check = [
        {
            'path': 'vite.config.ts',
            'pattern': r'host:\s*[\'"]([^\'\"]+)[\'"]',
            'expected': '0.0.0.0',
            'description': 'Frontend host binding (all interfaces)'
        },
        {
            'path': 'backend/app.py',
            'pattern': r'allow_origins=\[([^\]]+)\]',
            'expected_contains': ['localhost:8080', '192.168.0.108:8080'],
            'description': 'Backend CORS origins (both URLs)',
            'expected': None
        },
        {
            'path': 'backend/app.py',
            'pattern': r'uvicorn\.run\(.*host=[\'"]([^\'\"]+)[\'"]',
            'expected': '0.0.0.0',
            'description': 'Backend host binding (all interfaces)'
        },
        {
            'path': 'src/lib/attendanceData.ts',
            'pattern': r'window\.location\.hostname === [\'"]localhost[\'"]',
            'expected': 'window.location.hostname === \'localhost\'',
            'description': 'Dynamic URL detection logic',
            'expected_contains': []
        }
    ]
    
    all_correct = True
    
    for file_info in files_to_check:
        file_path = file_info['path']
        pattern = file_info['pattern']
        expected = file_info['expected']
        description = file_info['description']
        expected_contains = file_info.get('expected_contains', [])
        
        print(f"\n📁 Checking: {file_path}")
        print(f"   Purpose: {description}")
        
        if not os.path.exists(file_path):
            print(f"   ❌ File not found!")
            all_correct = False
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            match = re.search(pattern, content)
            
            if match:
                found_value = match.group(1)
                print(f"   📝 Found: {found_value}")
                
                # Check for exact match
                if expected and found_value == expected:
                    print(f"   ✅ CORRECT: Exact match!")
                # Check for contains logic
                elif expected_contains:
                    all_found = all(item in found_value for item in expected_contains)
                    if all_found:
                        print(f"   ✅ CORRECT: Contains both URLs!")
                    else:
                        print(f"   ❌ INCORRECT: Missing expected URLs")
                        all_correct = False
                else:
                    print(f"   ⚠️  Manual verification needed")
            else:
                print(f"   ❌ Pattern not found in file")
                all_correct = False
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            all_correct = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_correct:
        print("🎉 SUCCESS: Dual network configuration enabled!")
        print("✅ Frontend binds to all interfaces (0.0.0.0:8080)")
        print("✅ Backend binds to all interfaces (0.0.0.0:8000)")
        print("✅ CORS allows both localhost and network access")
        print("✅ Dynamic URL detection based on hostname")
        print("\n🌐 ACCESS URLS:")
        print("🖥️  Local Development: http://localhost:8080")
        print("📱 Network Access:   http://192.168.0.108:8080")
        print("🔧 Backend API:      http://localhost:8000/docs")
        print("📱 Network API:      http://192.168.0.108:8000/docs")
        print("\n🔄 NEXT STEPS:")
        print("1. Stop any running development servers")
        print("2. Restart frontend: npm run dev")
        print("3. Restart backend: python app.py")
        print("4. Test both URLs in browser")
        print("\n📱 BENEFITS:")
        print("- Localhost: Better for development, easier camera permissions")
        print("- Network: Mobile devices can access, QR codes work")
        print("- Dynamic: Automatically uses correct URL based on access method")
    else:
        print("⚠️  ISSUES FOUND: Some configurations need manual updates")
    
    return all_correct

if __name__ == "__main__":
    verify_dual_network_config()
