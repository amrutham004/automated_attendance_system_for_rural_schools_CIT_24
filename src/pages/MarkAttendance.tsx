import { useState } from 'react';
import Header from '@/components/attendance/Header';
import QRCodeDisplay from '@/components/attendance/QRCodeDisplay';
import StatusBadge from '@/components/attendance/StatusBadge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { markAttendance, getDailyToken } from '@/lib/attendanceData';
import { AttendanceStatus } from '@/types/attendance';
import { CheckCircle, XCircle, AlertCircle, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

type Step = 'input' | 'result';

interface ResultState {
  success: boolean;
  message: string;
  status?: AttendanceStatus;
}

const MarkAttendance = () => {
  const [step, setStep] = useState<Step>('input');
  const [studentId, setStudentId] = useState('');
  const [token, setToken] = useState('');
  const [result, setResult] = useState<ResultState | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate network delay
    setTimeout(() => {
      const response = markAttendance(studentId.toUpperCase(), token);
      setResult(response);
      setStep('result');
      setIsSubmitting(false);
    }, 500);
  };

  const handleReset = () => {
    setStep('input');
    setStudentId('');
    setToken('');
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container py-8 max-w-lg">
        <Button variant="ghost" size="sm" asChild className="mb-6">
          <Link to="/" className="flex items-center gap-2">
            <ArrowLeft size={16} />
            Back to Home
          </Link>
        </Button>

        {step === 'input' ? (
          <div className="space-y-6 animate-fade-in">
            <div className="text-center">
              <h1 className="text-2xl font-bold font-display mb-2">Mark Attendance</h1>
              <p className="text-muted-foreground">
                Enter your Student ID and today's attendance token
              </p>
            </div>

            {/* QR Code / Token Display */}
            <QRCodeDisplay />

            {/* Attendance Form */}
            <Card className="p-6 card-shadow">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label htmlFor="studentId">Student ID</Label>
                  <Input
                    id="studentId"
                    placeholder="e.g., STU001"
                    value={studentId}
                    onChange={(e) => setStudentId(e.target.value)}
                    required
                    className="text-center text-lg font-mono uppercase"
                  />
                  <p className="text-xs text-muted-foreground">
                    Demo IDs: STU001 - STU010
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="token">Attendance Token</Label>
                  <Input
                    id="token"
                    placeholder={`e.g., ${getDailyToken()}`}
                    value={token}
                    onChange={(e) => setToken(e.target.value)}
                    required
                    className="text-center text-lg font-mono"
                  />
                </div>

                <Button 
                  type="submit" 
                  className="w-full gradient-primary text-primary-foreground"
                  size="lg"
                  disabled={isSubmitting || !studentId || !token}
                >
                  {isSubmitting ? 'Recording...' : 'Record Attendance'}
                </Button>
              </form>
            </Card>
          </div>
        ) : (
          <div className="animate-scale-in">
            <Card className="p-8 card-shadow text-center">
              {result?.success ? (
                <div className="space-y-4">
                  <div className="w-20 h-20 mx-auto rounded-full bg-success/10 flex items-center justify-center">
                    <CheckCircle size={40} className="text-success" />
                  </div>
                  <h2 className="text-xl font-bold font-display text-success">Success!</h2>
                  <p className="text-muted-foreground">{result.message}</p>
                  {result.status && (
                    <div className="flex justify-center">
                      <StatusBadge status={result.status} />
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="w-20 h-20 mx-auto rounded-full bg-danger/10 flex items-center justify-center">
                    {result?.message.includes('already') ? (
                      <AlertCircle size={40} className="text-warning" />
                    ) : (
                      <XCircle size={40} className="text-danger" />
                    )}
                  </div>
                  <h2 className="text-xl font-bold font-display text-danger">
                    {result?.message.includes('already') ? 'Already Recorded' : 'Error'}
                  </h2>
                  <p className="text-muted-foreground">{result?.message}</p>
                </div>
              )}

              <div className="mt-8 space-y-3">
                <Button 
                  onClick={handleReset} 
                  className="w-full"
                  variant={result?.success ? 'outline' : 'default'}
                >
                  {result?.success ? 'Record Another' : 'Try Again'}
                </Button>
                <Button variant="ghost" className="w-full" asChild>
                  <Link to="/">Return to Home</Link>
                </Button>
              </div>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
};

export default MarkAttendance;
