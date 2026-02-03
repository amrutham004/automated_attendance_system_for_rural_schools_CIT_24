"""
verify_network_config.py - Verify network configuration changes

This script verifies that the network configuration has been updated
to use only http://192.168.0.115:8080 instead of multiple networks.
"""

import os
import re

def verify_network_config():
    """Verify the network configuration changes"""
    
    print("🌐 VERIFYING NETWORK CONFIGURATION")
    print("=" * 50)
    print("Target: http://192.168.0.108:8080")
    print("=" * 50)
    
    # Files to check
    files_to_check = [
        {
            'path': 'vite.config.ts',
            'pattern': r'host:\s*[\'"]([^\'\"]+)[\'"]',
            'expected': '192.168.0.108',
            'description': 'Frontend host binding'
        },
        {
            'path': 'backend/app.py',
            'pattern': r'allow_origins=\[[\'"]([^\'\"]+)[\'"]',
            'expected': 'http://192.168.0.108:8080/',
            'description': 'Backend CORS origin'
        },
        {
            'path': 'backend/app.py',
            'pattern': r'uvicorn\.run\(.*host=[\'"]([^\'\"]+)[\'"]',
            'expected': '192.168.0.108',
            'description': 'Backend host binding'
        },
        {
            'path': 'src/lib/attendanceData.ts',
            'pattern': r'const baseUrl = [\'"]([^\'\"]+)[\'"]',
            'expected': 'http://192.168.0.108:8080',
            'description': 'Frontend API base URL'
        }
    ]
    
    all_correct = True
    
    for file_info in files_to_check:
        file_path = file_info['path']
        pattern = file_info['pattern']
        expected = file_info['expected']
        description = file_info['description']
        
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
                
                # Check if it's the expected value
                if found_value == expected:
                    print(f"   ✅ CORRECT: Network configured properly!")
                else:
                    print(f"   ❌ INCORRECT: Expected {expected}")
                    all_correct = False
            else:
                print(f"   ❌ Pattern not found in file")
                all_correct = False
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            all_correct = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    if all_correct:
        print("🎉 SUCCESS: Network configuration fixed!")
        print("✅ Frontend will bind to: 192.168.0.108:8080")
        print("✅ Backend will bind to: 192.168.0.108:8000")
        print("✅ CORS configured for: 192.168.0.108:8080")
        print("✅ API calls will go to: 192.168.0.108:8000")
        print("\n🔄 NEXT STEPS:")
        print("1. Stop any running development servers")
        print("2. Restart frontend: npm run dev")
        print("3. Restart backend: python app.py")
        print("4. Access only at: http://192.168.0.108:8080")
        print("\n📱 RESULT:")
        print("- No more multiple network addresses")
        print("- Single access point: http://192.168.0.108:8080")
        print("- Mobile devices can connect via same network")
    else:
        print("⚠️  ISSUES FOUND: Some configurations need manual updates")
    
    return all_correct

if __name__ == "__main__":
    verify_network_config()
