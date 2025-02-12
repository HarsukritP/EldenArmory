import React from 'react';

interface NavbarProps {
  darkMode: boolean;
  onThemeToggle: () => void;
}


const Navbar: React.FC<NavbarProps> = ({ darkMode, onThemeToggle }) => {
  return (
    <nav className="bg-elden-lighter dark:bg-elden-dark border-b border-gray-200 dark:border-elden-accent px-4 py-3 transition-colors">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center gap-4">
            <img src="/EldenArmoury.png" alt="Elden Armory Logo" className="w-1/5 h-full object-contain" />
        </div>
        
        <button
          onClick={onThemeToggle}
          className="p-2 rounded-lg bg-gray-100 dark:bg-elden-accent/20 
                     hover:bg-gray-200 dark:hover:bg-elden-accent/30 
                     text-elden-dark dark:text-elden-gold transition-colors"
          aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? (
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="5"/>
              <line x1="12" y1="1" x2="12" y2="3"/>
              <line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/>
              <line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
            
          )}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;