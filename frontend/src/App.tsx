import React, { useState, useEffect } from 'react';
import WeaponList from './components/WeaponList';
import Navbar from './components/Navbar';

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(() => {
    // Check if window is defined (for SSR)
    if (typeof window !== 'undefined') {
      return document.documentElement.classList.contains('dark');
    }
    return false;
  });

  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [darkMode]);

  const handleThemeToggle = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className="min-h-screen bg-elden-light dark:bg-elden-darker transition-colors">
      <Navbar darkMode={darkMode} onThemeToggle={handleThemeToggle} />
      <main className="container mx-auto px-4 py-6">
        <WeaponList darkMode={darkMode} />
      </main>
    </div>
  );
};

export default App;