import { Link, useLocation } from 'react-router-dom';
import SchoolLogo from './SchoolLogo';
import { Button } from '@/components/ui/button';
import { Home, ClipboardCheck, LayoutDashboard, User, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Header = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/mark-attendance', label: 'Mark Attendance', icon: ClipboardCheck },
    { to: '/admin', label: 'Admin Dashboard', icon: LayoutDashboard },
    { to: '/student', label: 'Student Dashboard', icon: User },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 w-full bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/80 border-b border-border">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <SchoolLogo size="small" />
          <div className="hidden sm:block">
            <h1 className="text-lg font-bold font-display text-foreground">Rural School</h1>
            <p className="text-xs text-muted-foreground">Attendance System</p>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map(({ to, label, icon: Icon }) => (
            <Button
              key={to}
              variant={isActive(to) ? 'default' : 'ghost'}
              size="sm"
              asChild
            >
              <Link to={to} className="flex items-center gap-2">
                <Icon size={16} />
                {label}
              </Link>
            </Button>
          ))}
        </nav>

        {/* Mobile Menu Button */}
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
        </Button>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <nav className="md:hidden border-t border-border bg-card animate-fade-in">
          <div className="container py-3 space-y-1">
            {navLinks.map(({ to, label, icon: Icon }) => (
              <Button
                key={to}
                variant={isActive(to) ? 'default' : 'ghost'}
                className="w-full justify-start"
                asChild
                onClick={() => setMobileMenuOpen(false)}
              >
                <Link to={to} className="flex items-center gap-2">
                  <Icon size={18} />
                  {label}
                </Link>
              </Button>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
};

export default Header;
