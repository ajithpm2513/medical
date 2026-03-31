import { ShieldCheck, LogOut, Settings, HelpCircle, Bell } from 'lucide-react';
import { motion } from 'framer-motion';

const Navbar = ({ onLogout }) => {
  return (
    <nav className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-10 sticky top-0 z-50">
      <div className="flex items-center gap-4">
        <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center text-white shadow-lg shadow-primary/20 transition-transform hover:scale-105 cursor-pointer">
          <ShieldCheck size={24} />
        </div>
        <div>
          <h2 className="text-xl font-bold tracking-tight text-slate-900 leading-none">MedClassify</h2>
          <span className="text-[10px] uppercase font-bold text-slate-400 tracking-widest mt-1 block">Clinical Imaging Terminal</span>
        </div>
      </div>

      <div className="flex items-center gap-8">
        <div className="hidden md:flex items-center gap-6">
          <button className="text-slate-400 hover:text-primary transition-colors hover:bg-slate-50 p-2 rounded-lg relative">
            <Bell size={20} />
            <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full border-2 border-white"></span>
          </button>
          <button className="text-slate-400 hover:text-primary transition-colors hover:bg-slate-50 p-2 rounded-lg">
            <Settings size={20} />
          </button>
          <button className="text-slate-400 hover:text-primary transition-colors hover:bg-slate-50 p-2 rounded-lg">
            <HelpCircle size={20} />
          </button>
        </div>
        
        <div className="h-8 w-[1px] bg-slate-200"></div>

        <button 
          onClick={onLogout}
          className="btn-outline flex items-center gap-2 group border-primary/20 text-slate-600 hover:border-primary hover:text-primary py-2 px-4 text-sm"
        >
          <LogOut size={16} className="group-hover:-translate-x-1 transition-transform" />
          <span>Exit Console</span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
