"""
Setup Students Script
Automated Attendance System

This script seeds the database with the real students.
Run with: python setup_students.py
"""

import sqlite3
from pathlib import Path

# Database configuration
BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / 'data' / 'attendance.db'

def setup_students():
    """Connect to SQLite database and insert the three real students"""
    
    print("🔧 Setting up students database...")
    
    # Ensure data directory exists
    DB_FILE.parent.mkdir(exist_ok=True)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create students table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                grade TEXT,
                photo_path TEXT,
                has_face_encoding INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Real students to insert
        students = [
            ('20221CIT0043', 'Amrutha M', 'CIT 2022'),
            ('20221CIT0049', 'CM Shalini', 'CIT 2022'),
            ('20221CIT0151', 'Vismaya L', 'CIT 2022')
        ]
        
        # Insert or replace students
        for student_id, name, grade in students:
            cursor.execute('''
                INSERT OR REPLACE INTO students (student_id, name, grade)
                VALUES (?, ?, ?)
            ''', (student_id, name, grade))
            print(f"✅ Student {student_id} - {name} ({grade}) added/updated")
        
        # Commit changes
        conn.commit()
        
        # Verify insertion
        cursor.execute('SELECT student_id, name, grade FROM students ORDER BY student_id')
        all_students = cursor.fetchall()
        
        print(f"\n📊 Total students in database: {len(all_students)}")
        print("\n📋 Current Students:")
        for student in all_students:
            print(f"   {student[0]} - {student[1]} ({student[2]})")
        
        conn.close()
        print(f"\n✅ Students setup completed successfully!")
        print(f"📁 Database location: {DB_FILE}")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = setup_students()
    if success:
        print("\n🎉 Ready to start the attendance system!")
    else:
        print("\n❌ Setup failed. Please check the error above.")
