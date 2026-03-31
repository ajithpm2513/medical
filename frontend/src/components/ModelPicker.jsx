import { useState, useRef, useEffect } from 'react';
import { ChevronDown, Brain, Cpu, Database, Zap, Info, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ModelPicker = ({ models = [], selected, onSelect, isLoading }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Standard icon for models
  const ModelIcon = <Brain size={16} className="text-primary"/>;

  return (
    <div className="relative" ref={dropdownRef}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 bg-white border border-slate-200 px-5 py-2.5 rounded-full hover:bg-slate-50 transition-all shadow-sm group min-w-[240px]"
      >
        <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary shadow-sm shadow-primary/10 transition-transform group-hover:scale-110">
          {isLoading ? <Loader2 size={16} className="animate-spin" /> : (selected?.icon || ModelIcon)}
        </div>
        <div className="text-left pr-2 flex-1">
           <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-widest leading-none mb-1">Architecture</span>
           <span className="block text-sm font-bold text-slate-800 tracking-tight leading-none">
             {isLoading ? 'Scanning Cluster...' : (selected?.name || 'Select Weights')}
           </span>
        </div>
        <ChevronDown size={14} className={`text-slate-400 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            className="absolute top-full right-0 mt-4 w-80 bg-white rounded-2xl shadow-2xl border border-slate-100 p-3 z-[60] overflow-hidden"
          >
            <div className="p-3 border-b border-slate-100 mb-2 flex items-center justify-between">
                <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">Weight Discovery</span>
                <Info size={14} className="text-slate-300 pointer-events-none hover:text-primary transition-colors cursor-help" />
            </div>
            
            <div className="space-y-1 max-h-[400px] overflow-y-auto custom-scrollbar">
              {isLoading ? (
                <div className="p-12 flex flex-col items-center justify-center gap-4 text-center">
                   <Loader2 size={32} className="text-primary animate-spin" />
                   <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Scanning for models...</p>
                </div>
              ) : models.length > 0 ? (
                models.map((model) => (
                  <button
                    key={model.id}
                    onClick={() => { onSelect(model); setIsOpen(false); }}
                    className={`w-full flex items-start gap-4 p-4 rounded-xl transition-all ${selected?.id === model.id ? 'bg-primary/5 border border-primary/10' : 'hover:bg-slate-50 border border-transparent'}`}
                  >
                    <div className={`mt-1 p-2 rounded-lg ${selected?.id === model.id ? 'bg-primary/20 text-primary' : 'bg-slate-100 text-slate-400'}`}>
                      {ModelIcon}
                    </div>
                    <div className="text-left">
                      <span className={`block font-bold text-sm tracking-tight ${selected?.id === model.id ? 'text-primary' : 'text-slate-800'}`}>{model.name}</span>
                      <p className="text-[11px] text-slate-500 mt-1 font-medium leading-relaxed">
                        Arch: {model.architecture} ({model.extension})
                      </p>
                    </div>
                  </button>
                ))
              ) : (
                <div className="p-10 text-center">
                   <p className="text-sm text-slate-400 font-medium italic">No physical models detected in /models database.</p>
                </div>
              )}
            </div>
            
            <div className="mt-2 pt-3 border-t border-slate-100 px-3 pb-1">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Bridged to Local Research Storage</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ModelPicker;
