import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import { useState } from 'react';

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (e) => {
    setUser({ name: 'Clinical Specialist' });
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <Router>
      <div className="min-h-screen bg-slate-50">
        <Routes>
          <Route 
            path="/" 
            element={!user ? <LoginPage onLogin={handleLogin} /> : <Navigate to="/dashboard" />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? <DashboardPage onLogout={handleLogout} /> : <Navigate to="/" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
