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
      },
      backgroundImage: {
        timer: 'url("/static/images/timer.png")'
      },
      aspectRatio: {
        '188/451': '188 / 451', // カスタム比率
      },

    },
  },
  corePlugins: {
    aspectRatio: false,
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
}

