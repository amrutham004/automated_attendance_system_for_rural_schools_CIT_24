# Student Data Update

## Your Actual Student Information

```
Student 1:
- ID: 20221CIT0043
- Name: Amrutha M

Student 2:
- ID: 20221CIT0049
- Name: CM Shalini

Student 3:
- ID: 20221CIT0151
- Name: Vismaya L
```

---

## Update attendanceData.ts with Real Students

**File:** `src/lib/attendanceData.ts`

### Find and Update the Students Array

Replace the demo students with your real data:

```typescript
// BEFORE (Demo data)
export const students: Student[] = [
  { id: 'STU001', name: 'John Doe', grade: '10th' },
  { id: 'STU002', name: 'Jane Smith', grade: '11th' },
  // ... more demo students
];

// AFTER (Your real data)
export const students: Student[] = [
  { id: '20221CIT0043', name: 'Amrutha M', grade: 'CIT 2022' },
  { id: '20221CIT0049', name: 'CM Shalini', grade: 'CIT 2022' },
  { id: '20221CIT0151', name: 'Vismaya L', grade: 'CIT 2022' },
];
```

---

## Complete attendanceData.ts Student Section

```typescript
/**
 * Student data structure
 */
export interface Student {
  id: string;
  name: string;
  grade: string;
  email?: string;
  department?: string;
}

/**
 * Real student data - CIT 2022 Batch
 */
export const students: Student[] = [
  {
    id: '20221CIT0043',
    name: 'Amrutha M',
    grade: 'CIT 2022',
    department: 'Computer and Information Technology',
    email: 'amrutha.cit2022@example.com', // Optional
  },
  {
    id: '20221CIT0049',
    name: 'CM Shalini',
    grade: 'CIT 2022',
    department: 'Computer and Information Technology',
    email: 'shalini.cit2022@example.com', // Optional
  },
  {
    id: '20221CIT0151',
    name: 'Vismaya L',
    grade: 'CIT 2022',
    department: 'Computer and Information Technology',
    email: 'vismaya.cit2022@example.com', // Optional
  },
];
```

---

## Update Backend with Real Students

**File:** `backend/app.py` or create `backend/students_data.py`

### Option 1: Add to Backend Startup

```python
# In backend/app.py, after init_db()

def seed_initial_students():
    """Add initial students to database if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    initial_students = [
        ('20221CIT0043', 'Amrutha M', 'CIT 2022'),
        ('20221CIT0049', 'CM Shalini', 'CIT 2022'),
        ('20221CIT0151', 'Vismaya L', 'CIT 2022'),
    ]
    
    for student_id, name, grade in initial_students:
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO students (student_id, name, grade) VALUES (?, ?, ?)',
                (student_id, name, grade)
            )
        except Exception as e:
            print(f"Note: Student {student_id} may already exist")
    
    conn.commit()
    conn.close()
    print("✅ Initial students seeded")

# Call after init_db()
init_db()
seed_initial_students()  # Add this line
```

---

## Testing with Real Student IDs

### Test 1: Student Photo Upload
```python
# test_upload_real_students.py
import requests
import base64

BASE_URL = "http://localhost:8000"

students = [
    ("20221CIT0043", "Amrutha M", "test_photos/amrutha.jpg"),
    ("20221CIT0049", "CM Shalini", "test_photos/shalini.jpg"),
    ("20221CIT0151", "Vismaya L", "test_photos/vismaya.jpg"),
]

for student_id, name, photo_path in students:
    print(f"\nUploading photo for {name} ({student_id})...")
    
    with open(photo_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    payload = {
        "studentId": student_id,
        "studentName": name,
        "image": f"data:image/jpeg;base64,{image_base64}",
        "grade": "CIT 2022"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/admin/upload-student-photo",
        json=payload
    )
    
    if response.status_code == 200:
        print(f"✅ Success: {name}")
    else:
        print(f"❌ Failed: {response.json()}")
```

### Test 2: QR Code Generation

Now when you generate QR codes, use real IDs:

**In Mark Attendance page:**
```
Enter Student ID: 20221CIT0043
Click: Generate My QR Code
```

**Expected QR Code URL:**
```
http://YOUR_IP:8000/attendance/20221CIT0043/xyz123token
```

### Test 3: Face Recognition

```
Student ID: 20221CIT0043
Student Name: Amrutha M
Capture face → Verify → Attendance marked
```

---

## Update UI Placeholders

### In TeacherQRDisplay.tsx:

Find:
```typescript
<p className="text-xs text-cyan-200/60">
  Demo IDs: STU001 - STU010
</p>
```

Replace with:
```typescript
<p className="text-xs text-cyan-200/60">
  Valid IDs: 20221CIT0043, 20221CIT0049, 20221CIT0151
</p>
```

### In MarkAttendance.tsx:

Find:
```typescript
<p className="text-xs text-teal-200/60">
  Demo IDs: STU001 - STU010
</p>
```

Replace with:
```typescript
<p className="text-xs text-teal-200/60">
  Example: 20221CIT0043 (Amrutha M)
</p>
```

---

## Quick Database Setup Script

Create `backend/setup_students.py`:

```python
"""
Setup script to add real students to database
Run once to initialize student data
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / 'data' / 'attendance.db'

def setup_students():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    students = [
        {
            'id': '20221CIT0043',
            'name': 'Amrutha M',
            'grade': 'CIT 2022',
            'department': 'Computer and Information Technology'
        },
        {
            'id': '20221CIT0049',
            'name': 'CM Shalini',
            'grade': 'CIT 2022',
            'department': 'Computer and Information Technology'
        },
        {
            'id': '20221CIT0151',
            'name': 'Vismaya L',
            'grade': 'CIT 2022',
            'department': 'Computer and Information Technology'
        },
    ]
    
    for student in students:
        cursor.execute('''
            INSERT OR REPLACE INTO students 
            (student_id, name, grade, department, has_face_encoding)
            VALUES (?, ?, ?, ?, 0)
        ''', (student['id'], student['name'], student['grade'], student['department']))
        
        print(f"✅ Added: {student['name']} ({student['id']})")
    
    conn.commit()
    conn.close()
    
    print("\n✅ All students added to database!")
    print("\nNext steps:")
    print("1. Upload face photos for each student via admin panel")
    print("2. Test face recognition")
    print("3. Generate QR codes using real student IDs")

if __name__ == '__main__':
    print("=" * 60)
    print("SETTING UP REAL STUDENTS")
    print("=" * 60)
    setup_students()
```

Run it:
```bash
cd backend
python setup_students.py
```

---

## Prepare Student Photos

Create a folder for test photos:
```bash
mkdir test_photos
```

Take or prepare photos:
```
test_photos/
├── 20221CIT0043_amrutha.jpg
├── 20221CIT0049_shalini.jpg
└── 20221CIT0151_vismaya.jpg
```

**Photo Requirements:**
- Clear face visible
- Good lighting
- Front-facing
- One person only
- JPG or PNG format
- Recommended size: 640x480 or larger

---

## Complete Workflow with Real Students

### Step 1: Setup Students in Database
```bash
cd backend
python setup_students.py
```

### Step 2: Upload Face Photos (Admin Panel)
```
1. Go to Admin Dashboard
2. Student Photo Upload section
3. Select Student: 20221CIT0043 (Amrutha M)
4. Upload photo
5. Repeat for other students
```

### Step 3: Test QR Code
```
1. Go to Teacher QR Display
2. Enter: 20221CIT0043
3. Generate QR code
4. Scan with mobile (same WiFi)
5. Should redirect to face capture
```

### Step 4: Test Face Recognition
```
1. Go to Mark Attendance
2. Choose Face Recognition
3. Enter: 20221CIT0043
4. Capture face
5. Verify and mark attendance
```

---

## Updated Test Data

### For Frontend Testing (attendanceData.ts):

```typescript
// Update any demo attendance records
export const attendanceRecords: AttendanceRecord[] = [
  {
    id: 1,
    studentId: '20221CIT0043',
    studentName: 'Amrutha M',
    date: new Date().toISOString().split('T')[0],
    time: '09:15 AM',
    status: 'PRESENT',
    method: 'face_recognition'
  },
  // ... more records
];
```

---

## Student ID Format Notes

Your student IDs follow this pattern:
```
20221CIT0043
│││││││││││
│││││││└└└└─ Roll number (0043, 0049, 0151)
│││││└└───── Department code (CIT)
│└└└└─────── Admission year (2022)
└───────────── Prefix (2022)
```

**Validation pattern:**
```typescript
// Add to your validation logic
const STUDENT_ID_PATTERN = /^20221CIT\d{4}$/;

const isValidStudentId = (id: string) => {
  return STUDENT_ID_PATTERN.test(id);
};
```

---

## Summary of Changes

### Files to Update:

1. **`src/lib/attendanceData.ts`**
   - Replace demo students with real students
   - Update student IDs: STU001 → 20221CIT0043

2. **`backend/app.py`** (optional)
   - Add seed_initial_students() function
   - Seeds database with real students on startup

3. **UI Components**
   - Update placeholder text with real IDs
   - Update demo ID examples

4. **Test Scripts**
   - Use real student IDs in tests
   - Update photo paths

---

## Quick Commands

```bash
# 1. Update frontend students
# Edit: src/lib/attendanceData.ts

# 2. Setup backend students
cd backend
python setup_students.py

# 3. Restart servers
python app.py  # Backend
npm run dev    # Frontend

# 4. Test with real IDs
# Go to http://localhost:5173
# Enter: 20221CIT0043
```

---

## Testing Checklist

- [ ] Updated students array in attendanceData.ts
- [ ] Added students to backend database
- [ ] Updated UI placeholder text
- [ ] Prepared student photos
- [ ] Uploaded photos via admin panel
- [ ] Generated QR code with real ID
- [ ] Tested face recognition with real ID
- [ ] Verified attendance records show correct names

---

**You're all set with real student data!** 🎓

The system now works with:
- Amrutha M (20221CIT0043)
- CM Shalini (20221CIT0049)
- Vismaya L (20221CIT0151)

Need help with any of these steps? Let me know! 🚀