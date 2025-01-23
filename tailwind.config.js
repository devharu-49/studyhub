/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        rampartOne: ['Rampart One', 'sans-serif'],
        kosugiMaru: ['Kosugi Maru', 'sans-serif'],
      },
      colors: {
        menuColor: '#80a791', // メニューバーの色の追加
      },
    },
  },
  plugins: [],
}

