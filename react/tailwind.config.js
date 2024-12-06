module.exports = {
  content: ["./src/**/*.js", "./public/index.html"], // Specify the files where your Tailwind CSS classes are used
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        'custom-dark-gray': '#343131',
        'custom-red': '#A04747',
        'custom-gold': '#D8A25E',
        'custom-light-yellow': '#EEDF7A',
      },
    },
  },
  variants: {},
  plugins: [],
};