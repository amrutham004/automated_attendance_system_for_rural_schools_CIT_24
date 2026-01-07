import { Card } from '@/components/ui/card';
import { QrCode, Copy, Check } from 'lucide-react';
import { getDailyToken } from '@/lib/attendanceData';
import { useState } from 'react';
import { Button } from '@/components/ui/button';

const QRCodeDisplay = () => {
  const [copied, setCopied] = useState(false);
  const token = getDailyToken();

  const handleCopy = () => {
    navigator.clipboard.writeText(token);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card className="p-6 card-shadow text-center">
      <div className="space-y-4">
        <h3 className="text-lg font-semibold font-display">Today's Attendance Token</h3>
        
        {/* QR Code Placeholder */}
        <div className="mx-auto w-40 h-40 bg-muted rounded-xl flex items-center justify-center border-2 border-dashed border-border">
          <div className="text-center">
            <QrCode size={48} className="mx-auto text-muted-foreground mb-2" />
            <p className="text-xs text-muted-foreground">QR Code</p>
          </div>
        </div>

        {/* Token Display */}
        <div className="bg-secondary rounded-lg p-3">
          <p className="text-xs text-muted-foreground mb-1">Or enter token manually:</p>
          <div className="flex items-center justify-center gap-2">
            <code className="text-lg font-mono font-bold text-foreground">{token}</code>
            <Button 
              variant="ghost" 
              size="icon" 
              className="h-8 w-8"
              onClick={handleCopy}
            >
              {copied ? <Check size={16} className="text-success" /> : <Copy size={16} />}
            </Button>
          </div>
        </div>

        <p className="text-xs text-muted-foreground">
          This token changes daily. Share with students for attendance.
        </p>
      </div>
    </Card>
  );
};

export default QRCodeDisplay;
