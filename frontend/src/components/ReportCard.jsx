import { FileText, Printer, Share2, ClipboardCheck, Info, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ReportCard = ({ result, isLoading }) => {
  return (
    <div className="card h-full min-h-[500px] flex flex-col items-center justify-center p-8 bg-white border border-slate-200 shadow-xl overflow-hidden relative">
      <div className="absolute top-0 right-0 p-12 opacity-5 pointer-events-none">
          <FileText size={200} />
      </div>

      <AnimatePresence mode="wait">
        {isLoading ? (
          <motion.div 
            key="loading-report"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center gap-6 text-center z-10"
          >
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary relative">
                <div className="absolute inset-0 border-2 border-primary border-t-transparent rounded-2xl animate-spin"></div>
                <Activity size={32} />
            </div>
            <div className="space-y-2">
                <h3 className="text-xl font-bold text-slate-900 tracking-tight">Generating Clinical Insight</h3>
                <p className="text-slate-500 font-medium max-w-xs">Connecting to LLM Laboratory for automated radiological reporting...</p>
            </div>
            <div className="flex items-center gap-3">
               {[0, 1, 2].map((i) => (
                 <motion.div 
                    key={i}
                    animate={{ scale: [1, 1.3, 1], opacity: [0.3, 1, 0.3] }}
                    transition={{ repeat: Infinity, duration: 1.5, delay: i * 0.2 }}
                    className="w-2 h-2 rounded-full bg-primary"
                 />
               ))}
            </div>
          </motion.div>
        ) : result ? (
          <motion.div 
            key="report-content"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="w-full flex flex-col h-full z-10"
          >
            <header className="flex items-center justify-between mb-8 pb-4 border-b border-slate-100 pb-6">
               <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-slate-900 rounded-lg flex items-center justify-center text-white shadow-lg">
                     <ClipboardCheck size={24} />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-slate-800 tracking-tight uppercase leading-none mb-1">Clinical Report</h2>
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest block">Session ID: AI-293-8402</span>
                  </div>
               </div>
               
               <div className="flex gap-2">
                 <button className="p-2 hover:bg-slate-50 text-slate-400 hover:text-primary rounded-lg transition-colors" title="Print Report">
                    <Printer size={18} />
                 </button>
                 <button className="p-2 hover:bg-slate-50 text-slate-400 hover:text-primary rounded-lg transition-colors" title="Export JSON">
                    <Share2 size={18} />
                 </button>
               </div>
            </header>

            <div className="report-container flex-1 overflow-auto max-h-[550px] custom-scrollbar scroll-smooth">
               <div className="report-inner">
                  <div className="flex items-center justify-between mb-8 opacity-60">
                     <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Radiology Diagnostic Suite</span>
                     <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Date: {new Date().toLocaleDateString()}</span>
                  </div>

                  <div className="space-y-8">
                     <section>
                        <h4 className="text-[11px] font-bold text-primary uppercase tracking-widest mb-3 flex items-center gap-2">
                           <Info size={12} />
                           Primary Classification
                        </h4>
                        <div className="inline-block px-4 py-2 bg-primary/10 border border-primary/20 rounded text-primary font-bold text-lg tracking-tight">
                           {result.label}
                        </div>
                     </section>

                     <section>
                        <h4 className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-4">Laboratory Observations</h4>
                        <div className="text-slate-700 leading-relaxed font-serif text-sm bg-slate-50/50 p-6 rounded-lg border border-slate-100 italic">
                           {result.report.split('\n').map((line, i) => (
                             <p key={i} className="mb-4 last:mb-0">{line}</p>
                           ))}
                        </div>
                     </section>
                  </div>
                  
                  <div className="mt-12 pt-8 border-t border-slate-100 flex items-center justify-between opacity-50">
                      <div className="text-[9px] font-bold uppercase tracking-widest text-slate-400">Verified by Llama-3 Laboratory Inferencing System</div>
                      <div className="w-16 h-8 bg-slate-100 rounded flex items-center justify-center italic text-[10px] text-slate-400">Signature</div>
                  </div>
               </div>
            </div>
          </motion.div>
        ) : (
          <div className="flex flex-col items-center gap-6 text-center opacity-40">
            <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-300">
                <FileText size={40} />
            </div>
            <div className="space-y-1">
                <h3 className="text-lg font-bold text-slate-800 tracking-tight">Awaiting Analysis</h3>
                <p className="text-xs text-slate-500 font-medium max-w-[200px]">Upload a diagnostic image to generate a clinical laboratory report.</p>
            </div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ReportCard;
