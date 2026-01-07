import { Link } from 'react-router-dom';
import SchoolLogo from '@/components/attendance/SchoolLogo';
import Header from '@/components/attendance/Header';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ClipboardCheck, LayoutDashboard, Users, Clock } from 'lucide-react';
import { CUTOFF_TIME } from '@/lib/attendanceData';

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container py-8 md:py-12">
        {/* Hero Section */}
        <div className="text-center mb-10 md:mb-16 animate-fade-in">
          <div className="flex justify-center mb-6">
            <SchoolLogo size="large" />
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold font-display text-foreground mb-3">
            Rural School
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground mb-2">
            Automated Attendance System
          </p>
          <p className="text-sm text-muted-foreground flex items-center justify-center gap-2">
            <Clock size={14} />
            Cutoff time for on-time attendance: {CUTOFF_TIME} AM
          </p>
        </div>

        {/* Main CTA */}
        <div className="flex justify-center mb-12">
          <Button 
            size="lg" 
            className="gradient-primary text-primary-foreground px-8 py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
            asChild
          >
            <Link to="/mark-attendance" className="flex items-center gap-3">
              <ClipboardCheck size={24} />
              Mark Attendance
            </Link>
          </Button>
        </div>

        {/* Quick Access Cards */}
        <div className="grid md:grid-cols-2 gap-6 max-w-2xl mx-auto">
          <Card className="p-6 card-shadow hover:card-shadow-lg transition-all duration-200 hover:-translate-y-1">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-primary/10 text-primary">
                <LayoutDashboard size={24} />
              </div>
              <div className="flex-1">
                <h2 className="text-lg font-semibold font-display mb-1">Admin Dashboard</h2>
                <p className="text-sm text-muted-foreground mb-4">
                  View attendance statistics, reports, and manage student records.
                </p>
                <Button variant="outline" size="sm" asChild>
                  <Link to="/admin">Open Dashboard</Link>
                </Button>
              </div>
            </div>
          </Card>

          <Card className="p-6 card-shadow hover:card-shadow-lg transition-all duration-200 hover:-translate-y-1">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-accent text-accent-foreground">
                <Users size={24} />
              </div>
              <div className="flex-1">
                <h2 className="text-lg font-semibold font-display mb-1">Student Portal</h2>
                <p className="text-sm text-muted-foreground mb-4">
                  Check your attendance history and view your attendance percentage.
                </p>
                <Button variant="outline" size="sm" asChild>
                  <Link to="/student">View My Attendance</Link>
                </Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Features Section */}
        <div className="mt-16 text-center">
          <h2 className="text-xl font-semibold font-display mb-6 text-foreground">How It Works</h2>
          <div className="grid sm:grid-cols-3 gap-6 max-w-3xl mx-auto">
            <div className="p-4">
              <div className="w-12 h-12 rounded-full bg-primary/10 text-primary mx-auto mb-3 flex items-center justify-center font-bold font-display">
                1
              </div>
              <h3 className="font-medium mb-1">Enter Student ID</h3>
              <p className="text-sm text-muted-foreground">Students enter their unique ID</p>
            </div>
            <div className="p-4">
              <div className="w-12 h-12 rounded-full bg-primary/10 text-primary mx-auto mb-3 flex items-center justify-center font-bold font-display">
                2
              </div>
              <h3 className="font-medium mb-1">Enter Token</h3>
              <p className="text-sm text-muted-foreground">Scan QR or enter daily token</p>
            </div>
            <div className="p-4">
              <div className="w-12 h-12 rounded-full bg-primary/10 text-primary mx-auto mb-3 flex items-center justify-center font-bold font-display">
                3
              </div>
              <h3 className="font-medium mb-1">Attendance Recorded</h3>
              <p className="text-sm text-muted-foreground">Status updated automatically</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
