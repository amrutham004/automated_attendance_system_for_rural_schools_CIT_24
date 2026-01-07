interface AttendanceIndicatorProps {
  percentage: number;
  size?: 'small' | 'default' | 'large';
  showLabel?: boolean;
}

const AttendanceIndicator = ({ 
  percentage, 
  size = 'default',
  showLabel = true 
}: AttendanceIndicatorProps) => {
  const getStatus = () => {
    if (percentage >= 90) return { color: 'attendance-good', bg: 'bg-success', label: 'Excellent' };
    if (percentage >= 75) return { color: 'attendance-warning', bg: 'bg-warning', label: 'Needs Improvement' };
    return { color: 'attendance-critical', bg: 'bg-danger', label: 'Critical' };
  };

  const { color, bg, label } = getStatus();

  const sizeClasses = {
    small: { container: 'w-12 h-12', text: 'text-xs', ring: 'ring-2' },
    default: { container: 'w-20 h-20', text: 'text-lg', ring: 'ring-4' },
    large: { container: 'w-28 h-28', text: 'text-2xl', ring: 'ring-[6px]' },
  };

  const { container, text, ring } = sizeClasses[size];
  const circumference = 2 * Math.PI * 40;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className={`relative ${container}`}>
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="40"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-muted"
          />
          <circle
            cx="50"
            cy="50"
            r="40"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className={color}
            style={{ transition: 'stroke-dashoffset 0.5s ease-in-out' }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`${text} font-bold font-display ${color}`}>{percentage}%</span>
        </div>
      </div>
      {showLabel && (
        <span className={`text-xs font-medium ${color}`}>{label}</span>
      )}
    </div>
  );
};

export default AttendanceIndicator;
