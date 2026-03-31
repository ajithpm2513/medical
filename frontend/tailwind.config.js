/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0891b2', // cyan-600
          dark: '#0e7490', // cyan-700
          light: '#22d3ee', // cyan-400
          soft: '#ecfeff', // cyan-50
        },
        clinical: {
          white: '#ffffff',
          light: '#f8fafc',
          grey: '#cbd5e1',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
