/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#3b82f6",
        primaryDark: "#2563eb",

        background: "#f9fafb",
        backgroundDark: "#0f172a",

        text: "#111827",
        textDark: "#f9fafb",

        border: "#d1d5db",
        borderDark: "#334155",
      }
    },
  },
  plugins: [],
}

