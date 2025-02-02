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
        baseColor: '#f1f6f0', // 全体の背景色
        menuColor: '#80a791', // メニューバーの色
        activeMenuColor: '#9fc7aa', // 選択時のメニューバーの色
        card: "#dbeadb",
        "card-button": "#a6a6a6",
        "card-border": "#b2b3b0",
      },
    },
  },
  plugins: [],
}

