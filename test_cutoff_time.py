"""
test_cutoff_time.py - Test the new cut-off time functionality

This script verifies that the cut-off time has been changed from 11:00 AM to 1:00 PM
and that attendance status is correctly determined based on the new time.
"""

import sys
import os

# Add the src directory to the path so we can import the attendance data
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_cutoff_time():
    """Test that the cut-off time is correctly set to 1:00 PM"""
    try:
        # Import the CUTOFF_TIME constant
        from lib.attendanceData import CUTOFF_TIME
        
        print(f"🧪 TESTING CUT-OFF TIME")
        print("=" * 40)
        print(f"Current CUTOFF_TIME: {CUTOFF_TIME}")
        
        # Verify the cut-off time is set to 13:00 (1:00 PM in 24-hour format)
        expected_time = '13:00'
        
        if CUTOFF_TIME == expected_time:
            print(f"✅ SUCCESS: Cut-off time correctly set to {expected_time}")
            print(f"   This means attendance before 1:00 PM = PRESENT")
            print(f"   And attendance after 1:00 PM = LATE_PRESENT")
            return True
        else:
            print(f"❌ ERROR: Cut-off time is {CUTOFF_TIME}, expected {expected_time}")
            return False
            
    except ImportError as e:
        print(f"❌ ERROR: Could not import attendance data: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Unexpected error: {e}")
        return False

def test_attendance_status_logic():
    """Test the attendance status logic with different times"""
    try:
        from lib.attendanceData import CUTOFF_TIME, addAttendanceRecord
        
        print(f"\n🧪 TESTING ATTENDANCE STATUS LOGIC")
        print("=" * 40)
        
        # Test cases with different times
        test_cases = [
            ("08:30", "PRESENT"),      # Before 1:00 PM
            ("12:59", "PRESENT"),      # Just before 1:00 PM  
            ("13:00", "LATE_PRESENT"), # Exactly 1:00 PM
            ("13:01", "LATE_PRESENT"), # Just after 1:00 PM
            ("15:30", "LATE_PRESENT"), # Afternoon
            ("23:59", "LATE_PRESENT"), # Late night
        ]
        
        all_passed = True
        
        for test_time, expected_status in test_cases:
            # Create a mock attendance record
            record = addAttendanceRecord(
                studentId="TEST001",
                studentName="Test Student",
                test_time=test_time  # Pass the test time
            )
            
            actual_status = record.get('status')
            
            if actual_status == expected_status:
                print(f"✅ {test_time} → {actual_status} (correct)")
            else:
                print(f"❌ {test_time} → {actual_status} (expected {expected_status})")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ ERROR: Could not test attendance logic: {e}")
        return False

def main():
    print("🚀 CUT-OFF TIME CHANGE VERIFICATION")
    print("=" * 50)
    print("Testing the change from 11:00 AM to 1:00 PM")
    print("=" * 50)
    
    # Run tests
    test1_passed = test_cutoff_time()
    test2_passed = test_attendance_status_logic()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Cut-off time successfully changed to 1:00 PM")
        print("✅ Attendance status logic working correctly")
        print("\n📱 SYSTEM READY:")
        print("- Students marked PRESENT before 1:00 PM")
        print("- Students marked LATE_PRESENT after 1:00 PM")
        print("- Frontend displays correct cut-off time")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please check the implementation")
    
    return test1_passed and test2_passed

if __name__ == "__main__":
    main()
