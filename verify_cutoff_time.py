"""
verify_cutoff_time.py - Simple verification of cut-off time change

This script verifies that the cut-off time has been successfully changed 
from 11:00 AM to 1:00 PM by checking the actual source files.
"""

import os
import re

def verify_cutoff_time_change():
    """Verify the cut-off time change in the source files"""
    
    print("🚀 VERIFYING CUT-OFF TIME CHANGE")
    print("=" * 50)
    print("Checking: 11:00 AM → 1:00 PM")
    print("=" * 50)
    
    # Files to check
    files_to_check = [
        {
            'path': 'src/lib/attendanceData.ts',
            'pattern': r'export const CUTOFF_TIME = [\'"]([^\'\"]+)[\'"];',
            'description': 'Cut-off time constant'
        },
        {
            'path': 'src/pages/Index.tsx', 
            'pattern': r'Cutoff time: ([^<\n]+)',
            'description': 'Display text on home page'
        }
    ]
    
    all_correct = True
    
    for file_info in files_to_check:
        file_path = file_info['path']
        pattern = file_info['pattern']
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
                if '13:00' in found_value or '1:00 PM' in found_value:
                    print(f"   ✅ CORRECT: Cut-off time updated!")
                else:
                    print(f"   ❌ INCORRECT: Still showing old time")
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
        print("🎉 SUCCESS: Cut-off time successfully changed!")
        print("✅ Old time: 11:00 AM")
        print("✅ New time: 1:00 PM (13:00)")
        print("\n📱 IMPACT:")
        print("- Students marked PRESENT before 1:00 PM")
        print("- Students marked LATE_PRESENT after 1:00 PM")
        print("- Frontend displays updated cut-off time")
        print("\n🔄 NEXT STEPS:")
        print("1. Restart the frontend development server")
        print("2. Test attendance marking at different times")
        print("3. Verify the home page shows '1:00 PM'")
    else:
        print("⚠️  ISSUES FOUND: Some files may need manual updates")
    
    return all_correct

if __name__ == "__main__":
    verify_cutoff_time_change()
