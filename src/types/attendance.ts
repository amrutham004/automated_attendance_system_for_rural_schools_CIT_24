export type AttendanceStatus = 'PRESENT' | 'LATE_PRESENT' | 'ABSENT';

export interface Student {
  id: string;
  name: string;
  grade: string;
}

export interface AttendanceRecord {
  studentId: string;
  studentName: string;
  date: string;
  time: string;
  status: AttendanceStatus;
}

export interface AttendanceConfig {
  cutoffTime: string; // HH:MM format
}

export interface DashboardStats {
  totalStudents: number;
  presentToday: number;
  lateToday: number;
  absentToday: number;
}

export interface StudentStats {
  totalDays: number;
  daysPresent: number;
  daysLate: number;
  daysAbsent: number;
  attendancePercentage: number;
}
