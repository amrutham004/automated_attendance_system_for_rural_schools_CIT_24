import { useState } from 'react';
import Header from '@/components/attendance/Header';
import StatCard from '@/components/attendance/StatCard';
import StatusBadge from '@/components/attendance/StatusBadge';
import AttendanceIndicator from '@/components/attendance/AttendanceIndicator';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  getStudentStats, 
  getStudentById, 
  getAttendanceRecords,
  students 
} from '@/lib/attendanceData';
import { StudentStats, Student } from '@/types/attendance';
import { CalendarCheck, CalendarX, Clock, Search, User } from 'lucide-react';

const StudentDashboard = () => {
  const [studentId, setStudentId] = useState('');
  const [searchedStudent, setSearchedStudent] = useState<Student | null>(null);
  const [stats, setStats] = useState<StudentStats | null>(null);
  const [error, setError] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    const student = getStudentById(studentId.toUpperCase());
    if (!student) {
      setError('Student ID not found. Please check and try again.');
      setSearchedStudent(null);
      setStats(null);
      return;
    }

    setSearchedStudent(student);
    setStats(getStudentStats(student.id));
  };

  const studentRecords = searchedStudent 
    ? getAttendanceRecords()
        .filter(r => r.studentId === searchedStudent.id)
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
        .slice(0, 10)
    : [];

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container py-8 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-2xl md:text-3xl font-bold font-display mb-2">Student Dashboard</h1>
          <p className="text-muted-foreground">
            View your attendance history and statistics
          </p>
        </div>

        {/* Search Form */}
        <Card className="p-6 card-shadow mb-8">
          <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 space-y-2">
              <Label htmlFor="studentSearch">Enter Your Student ID</Label>
              <Input
                id="studentSearch"
                placeholder="e.g., STU001"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="font-mono uppercase"
              />
              <p className="text-xs text-muted-foreground">
                Demo IDs: {students.slice(0, 3).map(s => s.id).join(', ')}...
              </p>
            </div>
            <div className="flex items-end">
              <Button type="submit" disabled={!studentId}>
                <Search size={16} className="mr-2" />
                View Dashboard
              </Button>
            </div>
          </form>
          {error && (
            <p className="mt-4 text-sm text-danger">{error}</p>
          )}
        </Card>

        {/* Student Info */}
        {searchedStudent && stats && (
          <div className="animate-fade-in space-y-6">
            {/* Student Header */}
            <Card className="p-6 card-shadow">
              <div className="flex flex-col sm:flex-row items-center gap-6">
                <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center">
                  <User size={36} className="text-primary" />
                </div>
                <div className="text-center sm:text-left flex-1">
                  <h2 className="text-xl font-bold font-display">{searchedStudent.name}</h2>
                  <p className="text-muted-foreground">
                    ID: {searchedStudent.id} • Grade: {searchedStudent.grade}
                  </p>
                </div>
                <AttendanceIndicator percentage={stats.attendancePercentage} size="large" />
              </div>
            </Card>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard
                title="Total Days"
                value={stats.totalDays}
                subtitle="Last 30 days"
                icon={CalendarCheck}
                variant="default"
              />
              <StatCard
                title="Days Present"
                value={stats.daysPresent}
                icon={CalendarCheck}
                variant="success"
              />
              <StatCard
                title="Days Late"
                value={stats.daysLate}
                icon={Clock}
                variant="warning"
              />
              <StatCard
                title="Days Absent"
                value={stats.daysAbsent}
                icon={CalendarX}
                variant="danger"
              />
            </div>

            {/* Attendance Percentage Visual */}
            <Card className="p-6 card-shadow">
              <h3 className="font-semibold font-display mb-4">Attendance Status</h3>
              <div className="flex items-center gap-4">
                <div className="flex-1">
                  <div className="h-4 bg-muted rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-500 ${
                        stats.attendancePercentage >= 90 
                          ? 'bg-success' 
                          : stats.attendancePercentage >= 75 
                            ? 'bg-warning' 
                            : 'bg-danger'
                      }`}
                      style={{ width: `${stats.attendancePercentage}%` }}
                    />
                  </div>
                </div>
                <span className={`font-bold text-lg ${
                  stats.attendancePercentage >= 90 
                    ? 'text-success' 
                    : stats.attendancePercentage >= 75 
                      ? 'text-warning' 
                      : 'text-danger'
                }`}>
                  {stats.attendancePercentage}%
                </span>
              </div>
              <div className="mt-4 flex flex-wrap gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-success" />
                  <span>≥90% Excellent</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-warning" />
                  <span>75-89% Needs Improvement</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-danger" />
                  <span>&lt;75% Critical</span>
                </div>
              </div>
            </Card>

            {/* Recent Records */}
            <Card className="card-shadow">
              <div className="p-6 border-b border-border">
                <h3 className="font-semibold font-display">Recent Attendance Records</h3>
              </div>
              {studentRecords.length > 0 ? (
                <div className="divide-y divide-border">
                  {studentRecords.map((record, index) => (
                    <div key={index} className="px-6 py-4 flex items-center justify-between hover:bg-muted/30 transition-colors">
                      <div>
                        <p className="font-medium">
                          {new Date(record.date).toLocaleDateString('en-US', {
                            weekday: 'short',
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric'
                          })}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          Time: {record.time || '-'}
                        </p>
                      </div>
                      <StatusBadge status={record.status} size="small" />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-muted-foreground">
                  No attendance records found
                </div>
              )}
            </Card>
          </div>
        )}

        {/* Empty State */}
        {!searchedStudent && !error && (
          <div className="text-center py-12 text-muted-foreground">
            <User size={48} className="mx-auto mb-4 opacity-30" />
            <p>Enter your Student ID above to view your attendance dashboard</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default StudentDashboard;
