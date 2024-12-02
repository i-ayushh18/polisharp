/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
	  extend: {
      fontFamily: {
        'display': ['Parkinsans', 'sans-serif'],
        'cursive': ['Playwrite HR Lijeva', 'cursive']
      }
    },
  },
  plugins: [],
}

