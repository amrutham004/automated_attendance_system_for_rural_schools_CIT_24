import { GraduationCap } from 'lucide-react';

const SchoolLogo = ({ size = 'default' }: { size?: 'small' | 'default' | 'large' }) => {
  const sizeClasses = {
    small: 'w-10 h-10',
    default: 'w-16 h-16',
    large: 'w-24 h-24',
  };

  const iconSizes = {
    small: 20,
    default: 32,
    large: 48,
  };

  return (
    <div className={`${sizeClasses[size]} rounded-full gradient-primary flex items-center justify-center card-shadow-lg`}>
      <GraduationCap className="text-primary-foreground" size={iconSizes[size]} />
    </div>
  );
};

export default SchoolLogo;
