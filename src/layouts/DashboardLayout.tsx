import { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  Heart, 
  LayoutDashboard, 
  Map, 
  Sparkles, 
  FolderOpen, 
  CalendarCheck, 
  Bell, 
  User, 
  UploadCloud, 
  LogOut, 
  Menu, 
  X 
} from 'lucide-react';

export default function DashboardLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const isBypassEnabled = !import.meta.env.PROD && import.meta.env.VITE_DEV_BYPASS_AUTH === 'true';

  // Example active route check
  const isActive = (path: string) => location.pathname === path;

  const handleLogout = () => {
    // Implement token clearing here
    localStorage.removeItem('carepath_token');
    localStorage.removeItem('carepath_patient_id');
    navigate('/login');
  };

  const menuItems = [
    { name: 'Overview', path: '/dashboard', icon: LayoutDashboard },
    { name: 'My Journey', path: '/journey', icon: Map },
    { name: 'AI Analysis', path: '/analysis', icon: Sparkles },
    { name: 'Upload Center', path: '/upload', icon: UploadCloud },
    { name: 'My Records', path: '/records', icon: FolderOpen },
    { name: 'Follow-up', path: '/followup', icon: CalendarCheck },
  ];

  const secondaryItems = [
    { name: 'Notifications', path: '/notifications', icon: Bell },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  return (
    <div className="min-h-screen flex bg-brand-bg font-sans text-brand-plum">
      {/* Desktop Sidebar */}
      <aside 
        className={`hidden md:flex flex-col justify-between sticky top-0 h-screen transition-all duration-300 ease-in-out bg-brand-card border-r border-brand-slate/10 shrink-0 ${
          isCollapsed ? 'w-20 px-3 py-6' : 'w-64 p-6'
        }`}
      >
        <div className="flex flex-col gap-8">
          {/* Logo acting as toggle */}
          <button 
            onClick={() => setIsCollapsed(!isCollapsed)}
            className={`flex items-center gap-2.5 group cursor-pointer text-left focus:outline-none w-full ${
              isCollapsed ? 'justify-center' : ''
            }`}
          >
            <div className="w-9 h-9 rounded-xl bg-brand-lavender flex items-center justify-center text-white transition-transform group-hover:scale-105 shrink-0">
              <Heart className="w-5 h-5 fill-current" />
            </div>
            {!isCollapsed && (
              <div className="animate-in fade-in duration-200">
                <span className="font-display font-bold text-xl tracking-tight text-brand-plum">CarePath</span>
                <span className="text-brand-lavender font-bold text-sm ml-0.5">AI</span>
              </div>
            )}
          </button>

          {/* Navigation Links */}
          <nav className="flex flex-col gap-1">
            {!isCollapsed ? (
              <span className="text-xs font-semibold tracking-wider text-brand-slate/75 uppercase px-3 mb-2 animate-in fade-in duration-200">Navigation</span>
            ) : (
              <div className="h-px bg-brand-slate/10 my-2" />
            )}
            {menuItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  title={isCollapsed ? item.name : undefined}
                  aria-label={item.name}
                  className={`flex items-center rounded-xl text-sm font-medium transition-all relative group/link ${
                    isCollapsed 
                      ? 'justify-center w-10 h-10 mx-auto' 
                      : 'gap-3 px-3 py-2.5'
                  } ${
                    active 
                      ? 'bg-brand-lavender-light text-brand-lavender shadow-sm font-semibold' 
                      : 'text-brand-slate hover:bg-brand-bg hover:text-brand-plum'
                  }`}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${active ? 'text-brand-lavender' : ''}`} />
                  {!isCollapsed && <span className="animate-in fade-in duration-200">{item.name}</span>}
                  
                  {isCollapsed && (
                    <div className="absolute left-full ml-3 px-2 py-1 bg-brand-plum text-white text-xxs rounded-md opacity-0 pointer-events-none group-hover/link:opacity-100 transition-opacity whitespace-nowrap z-50 shadow-sm">
                      {item.name}
                    </div>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Bottom items */}
        <div className="flex flex-col gap-4">
          <nav className="flex flex-col gap-1 border-t border-brand-slate/10 pt-4">
            {secondaryItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  title={isCollapsed ? item.name : undefined}
                  aria-label={item.name}
                  className={`flex items-center rounded-xl text-sm font-medium transition-all relative group/link ${
                    isCollapsed 
                      ? 'justify-center w-10 h-10 mx-auto' 
                      : 'gap-3 px-3 py-2.5'
                  } ${
                    active 
                      ? 'bg-brand-lavender-light text-brand-lavender shadow-sm font-semibold' 
                      : 'text-brand-slate hover:bg-brand-bg hover:text-brand-plum'
                  }`}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${active ? 'text-brand-lavender' : ''}`} />
                  {!isCollapsed && <span className="animate-in fade-in duration-200">{item.name}</span>}
                  
                  {isCollapsed && (
                    <div className="absolute left-full ml-3 px-2 py-1 bg-brand-plum text-white text-xxs rounded-md opacity-0 pointer-events-none group-hover/link:opacity-100 transition-opacity whitespace-nowrap z-50 shadow-sm">
                      {item.name}
                    </div>
                  )}
                </Link>
              );
            })}
            <button
              onClick={handleLogout}
              title={isCollapsed ? "Sign Out" : undefined}
              aria-label="Sign Out"
              className={`flex items-center rounded-xl text-sm font-medium text-brand-rose-text hover:bg-brand-rose-bg/50 transition-all text-left mt-1 relative group/link ${
                isCollapsed 
                  ? 'justify-center w-10 h-10 mx-auto' 
                  : 'gap-3 px-3 py-2.5 w-full'
              }`}
            >
              <LogOut className="w-4 h-4 text-brand-rose-text shrink-0" />
              {!isCollapsed && <span className="animate-in fade-in duration-200">Sign Out</span>}
              
              {isCollapsed && (
                <div className="absolute left-full ml-3 px-2 py-1 bg-brand-rose-text text-white text-xxs rounded-md opacity-0 pointer-events-none group-hover/link:opacity-100 transition-opacity whitespace-nowrap z-50 shadow-sm">
                  Sign Out
                </div>
              )}
            </button>
          </nav>
        </div>
      </aside>

      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden bg-brand-plum/45 backdrop-blur-sm">
          <div className="w-64 bg-brand-card h-full p-6 flex flex-col justify-between animate-in slide-in-from-left duration-250">
            <div className="flex flex-col gap-8">
              <div className="flex items-center justify-between">
                <button 
                  onClick={() => setMobileMenuOpen(false)} 
                  className="flex items-center gap-2.5 text-left focus:outline-none cursor-pointer hover:opacity-85"
                >
                  <div className="w-8 h-8 rounded-lg bg-brand-lavender flex items-center justify-center text-white">
                    <Heart className="w-4.5 h-4.5 fill-current animate-in zoom-in-50" />
                  </div>
                  <span className="font-display font-bold text-lg text-brand-plum">CarePath AI</span>
                </button>
                <button 
                  onClick={() => setMobileMenuOpen(false)}
                  className="p-1 rounded-lg hover:bg-brand-bg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <nav className="flex flex-col gap-1">
                {menuItems.map((item) => {
                  const Icon = item.icon;
                  const active = isActive(item.path);
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        active 
                          ? 'bg-brand-lavender-light text-brand-lavender font-semibold' 
                          : 'text-brand-slate hover:bg-brand-bg hover:text-brand-plum'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>

            <div className="flex flex-col gap-4">
              <nav className="flex flex-col gap-1 border-t border-brand-slate/10 pt-4">
                {secondaryItems.map((item) => {
                  const Icon = item.icon;
                  const active = isActive(item.path);
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        active 
                          ? 'bg-brand-lavender-light text-brand-lavender font-semibold' 
                          : 'text-brand-slate hover:bg-brand-bg'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout();
                  }}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-brand-rose-text hover:bg-brand-rose-bg/50 transition-all text-left w-full mt-1"
                >
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out">
        {/* Mobile Header */}
        <header className="flex md:hidden items-center justify-between bg-brand-card border-b border-brand-slate/10 px-6 py-4 sticky top-0 z-30">
          <button 
            onClick={() => setMobileMenuOpen(true)}
            className="p-1 rounded-lg hover:bg-brand-bg text-brand-slate"
          >
            <Menu className="w-6 h-6" />
          </button>
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="font-display font-semibold text-brand-plum flex items-center gap-1.5 focus:outline-none cursor-pointer hover:opacity-85 active:scale-98 transition-all"
          >
            <Heart className="w-4 h-4 text-brand-lavender fill-current shrink-0" />
            <span>CarePath AI</span>
          </button>
          <Link to="/notifications" className="p-1 rounded-lg hover:bg-brand-bg text-brand-slate relative">
            <Bell className="w-5 h-5" />
          </Link>
        </header>

        {/* Dashboard Content Container */}
        <main className="flex-1 p-6 md:p-8 max-w-6xl w-full mx-auto animate-in fade-in duration-300">
          <Outlet />
        </main>
      </div>

      {isBypassEnabled && (
        <div className="fixed bottom-4 right-4 z-50 bg-brand-amber-bg border border-brand-amber-text/20 text-brand-amber-text text-xxs font-bold px-3.5 py-2 rounded-full shadow-md flex items-center gap-2 pointer-events-none select-none">
          <span className="w-2 h-2 rounded-full bg-brand-amber-text animate-pulse shrink-0"></span>
          <span>Development Mode (Auth Bypass)</span>
        </div>
      )}
    </div>
  );
}
