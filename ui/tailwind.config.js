/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        'wiggle': 'wiggle 0.25s ease-in-out infinite'
      },
      keyframes: {
        wiggle: {
          '0%': { 'transform': 'translateX(0)' },
          '25%': { 'transform': 'translateX(0.5px)' },
          '50%': { 'transform': 'translateX(-0.5px)' },
          '75%': { 'transform': 'translateX(0.5px)' },
          '100%': { 'transform': 'translateX(0)' }
        }
      }
    },
  },
  plugins: [],
};
