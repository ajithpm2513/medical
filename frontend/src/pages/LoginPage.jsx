import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Stethoscope, ShieldCheck, Mail, Lock } from 'lucide-react';

const LoginPage = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin();
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-slate-50 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 p-24 opacity-5 pointer-events-none">
        <Stethoscope size={400} />
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl border border-slate-200 z-10"
      >
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 bg-primary rounded-xl flex items-center justify-center mb-4 text-white shadow-lg shadow-primary/20">
            <ShieldCheck size={32} />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            MedClassify <span className="text-primary font-medium text-lg">PRO</span>
          </h1>
          <p className="text-slate-500 text-sm">Professional MRI Diagnostic Suite</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Corporate Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="dr.care@hospital.com"
                className="input-field pl-10"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="input-field pl-10"
                required
              />
            </div>
          </div>

          <button type="submit" className="w-full btn-primary h-12 text-sm uppercase tracking-widest font-bold">
            {isRegistering ? 'Initialize Account' : 'Authenticate Console'}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-slate-100 text-center">
          <button 
            onClick={() => setIsRegistering(!isRegistering)}
            className="text-primary hover:text-primary-dark font-medium transition-colors text-sm"
          >
            {isRegistering 
              ? 'Already registered? Access your terminal' 
              : 'New practitioner? Request access'
            }
          </button>
        </div>
      </motion.div>
      
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 text-slate-400 text-xs font-medium">
        © 2026 MedClassify Digital Pathology Systems. All Rights Reserved.
      </div>
    </div>
  );
};

export default LoginPage;
