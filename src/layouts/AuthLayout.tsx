import { Outlet, Link } from 'react-router-dom';
import { Heart } from 'lucide-react';

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-brand-bg font-sans">
      {/* Left branding pane */}
      <div className="hidden md:flex md:w-1/2 bg-brand-plum text-white flex-col justify-between p-12 relative overflow-hidden">
        {/* Subtle background circles for premium visual detail */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-lavender/10 rounded-full blur-3xl -translate-y-12 translate-x-12 pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-brand-lavender/5 rounded-full blur-3xl translate-y-12 -translate-x-12 pointer-events-none" />

        <Link to="/" className="flex items-center gap-2.5 group relative z-10">
          <div className="w-10 h-10 rounded-xl bg-brand-lavender flex items-center justify-center text-white transition-transform group-hover:scale-105">
            <Heart className="w-6 h-6 fill-current" />
          </div>
          <div>
            <span className="font-display font-bold text-2xl tracking-tight text-white">CarePath</span>
            <span className="text-brand-lavender-light font-bold text-sm ml-0.5">AI</span>
          </div>
        </Link>

        <div className="max-w-md my-auto relative z-10">
          <h1 className="font-display text-4xl font-semibold leading-tight text-white mb-6">
            Your healthcare journey, clearly mapped.
          </h1>
          <p className="text-white/70 text-lg leading-relaxed font-light">
            CarePath AI matches symptoms, analyzes medical documents, and charts a personalized, step-by-step path to the right specialist.
          </p>
        </div>

        <div className="text-xs text-white/40 relative z-10">
          CarePath AI provides healthcare navigation support. We do not provide medical diagnosis.
        </div>
      </div>

      {/* Right form container */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md bg-brand-card rounded-2xl border border-brand-slate/10 p-8 shadow-sm">
          {/* Logo visible only on mobile */}
          <div className="flex md:hidden items-center justify-center gap-2 mb-8">
            <div className="w-9 h-9 rounded-lg bg-brand-lavender flex items-center justify-center text-white">
              <Heart className="w-5 h-5 fill-current" />
            </div>
            <span className="font-display font-bold text-xl text-brand-plum">CarePath AI</span>
          </div>

          <Outlet />
        </div>
      </div>
    </div>
  );
}
