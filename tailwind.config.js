/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/index.html",
    "./static/js/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        'patrick-hand': ['"Patrick Hand"', 'cursive']
      }
    }
  },
  plugins: [],
}