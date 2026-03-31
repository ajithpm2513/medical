import { Upload, ImageIcon, FileText, ChevronRight, X } from 'lucide-react';
import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const FileUpload = ({ onUpload }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onUpload(files[0]);
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      onUpload(files[0]);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`mri-dropzone relative group min-h-[450px] bg-white border-2 border-dashed border-slate-200 hover:border-primary/50 hover:bg-primary/[0.02] transition-all duration-300 rounded-3xl overflow-hidden flex flex-col items-center justify-center cursor-pointer ${isDragging ? 'border-primary bg-primary/5 scale-[1.01]' : 'border-slate-300'}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <input 
        type="file" 
        ref={fileInputRef} 
        className="hidden" 
        accept="image/*"
        onChange={handleFileChange}
      />

      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary/20 to-transparent group-hover:from-primary/10 group-hover:via-primary/50 group-hover:to-primary/10 transition-all"></div>

      <div className="flex flex-col items-center gap-4 text-center p-12 max-w-lg">
        <div className="w-20 h-20 rounded-2xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary/10 group-hover:text-primary transition-all duration-300 relative">
          <Upload size={32} />
          <motion.div 
            animate={{ y: [0, -4, 0] }}
            transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
            className="absolute -top-1 -right-1 w-6 h-6 bg-primary rounded-full flex items-center justify-center text-white text-[10px] shadow-lg shadow-primary/20"
          >
            <ChevronRight size={12} />
          </motion.div>
        </div>

        <div className="space-y-2 mt-4">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Initiate Diagnostic Scan</h2>
          <p className="text-slate-500 font-medium">Please upload MRI scan imagery in DICOM, JPEG, or PNG format for neural architecture analysis.</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mt-8 w-full max-w-sm">
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 flex items-center gap-3">
             <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-slate-400 shadow-sm">
                <ImageIcon size={18} />
             </div>
             <div className="text-left">
                <span className="block text-xs font-bold text-slate-700 uppercase">Imaging</span>
                <span className="block text-[10px] text-slate-400 uppercase font-medium mt-1 tracking-wider">Hi-Res Imagery</span>
             </div>
          </div>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 flex items-center gap-3">
             <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-slate-400 shadow-sm">
                <FileText size={18} />
             </div>
             <div className="text-left">
                <span className="block text-xs font-bold text-slate-700 uppercase">DICOM</span>
                <span className="block text-[10px] text-slate-400 uppercase font-medium mt-1 tracking-wider">Metadata Sync</span>
             </div>
          </div>
        </div>
        
        <div className="mt-8 flex items-center gap-4">
            <span className="text-xs text-slate-400 font-medium uppercase tracking-[3px]">Select File</span>
            <div className="h-[1px] w-8 bg-slate-200"></div>
            <span className="text-xs text-slate-400 font-medium uppercase tracking-[3px]">or Drag & Drop</span>
        </div>
      </div>
    </motion.div>
  );
};

export default FileUpload;
