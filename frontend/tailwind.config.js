/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        screens: {
          'sm': '640px',
          'md': '768px',
          'lg': '1024px',
          'xl': '1280px',
          '2xl': '1536px',
        },
        'elden': {
          gold: '#C7A84C',
          dark: '#1A1A1D',
          darker: '#15151A',
          light: '#F5F5F7',
          lighter: '#FFFFFF',
          accent: '#554A2B',
          'text-light': '#2D2D30',
          'text-dark': '#9C8E6B',
        }
      }
    },
  },
  plugins: [],
}