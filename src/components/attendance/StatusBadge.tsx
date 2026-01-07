import { AttendanceStatus } from '@/types/attendance';
import { CheckCircle, Clock, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: AttendanceStatus;
  size?: 'small' | 'default';
}

const StatusBadge = ({ status, size = 'default' }: StatusBadgeProps) => {
  const config = {
    PRESENT: {
      label: 'Present',
      className: 'status-present',
      icon: CheckCircle,
    },
    LATE_PRESENT: {
      label: 'Late',
      className: 'status-late',
      icon: Clock,
    },
    ABSENT: {
      label: 'Absent',
      className: 'status-absent',
      icon: XCircle,
    },
  };

  const { label, className, icon: Icon } = config[status];
  const sizeClasses = size === 'small' 
    ? 'px-2 py-0.5 text-xs gap-1' 
    : 'px-3 py-1 text-sm gap-1.5';

  return (
    <span className={`inline-flex items-center ${sizeClasses} ${className} rounded-full font-medium`}>
      <Icon size={size === 'small' ? 12 : 14} />
      {label}
    </span>
  );
};

export default StatusBadge;
