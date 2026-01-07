import { LucideIcon } from 'lucide-react';
import { Card } from '@/components/ui/card';

interface StatCardProps {
  title: string;
  value: number | string;
  subtitle?: string;
  icon: LucideIcon;
  variant?: 'default' | 'success' | 'warning' | 'danger';
}

const StatCard = ({ title, value, subtitle, icon: Icon, variant = 'default' }: StatCardProps) => {
  const variantClasses = {
    default: 'bg-primary/10 text-primary',
    success: 'bg-success/10 text-success',
    warning: 'bg-warning/10 text-warning',
    danger: 'bg-danger/10 text-danger',
  };

  return (
    <Card className="p-4 sm:p-6 card-shadow hover:card-shadow-lg transition-shadow duration-200">
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-sm text-muted-foreground font-medium">{title}</p>
          <p className="text-2xl sm:text-3xl font-bold font-display">{value}</p>
          {subtitle && (
            <p className="text-xs text-muted-foreground">{subtitle}</p>
          )}
        </div>
        <div className={`p-2.5 rounded-lg ${variantClasses[variant]}`}>
          <Icon size={22} />
        </div>
      </div>
    </Card>
  );
};

export default StatCard;
