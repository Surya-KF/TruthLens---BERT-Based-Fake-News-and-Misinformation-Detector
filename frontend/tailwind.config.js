/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      colors: {
        pro: {
          bg:      'rgb(var(--color-bg) / <alpha-value>)',
          surface: 'rgb(var(--color-surface) / <alpha-value>)',
          card:    'rgb(var(--color-card) / <alpha-value>)',
          text:    'rgb(var(--color-text) / <alpha-value>)',
          sub:     'rgb(var(--color-sub) / <alpha-value>)',
          blue:    'rgb(var(--color-accent1) / <alpha-value>)',
          border:  'rgb(var(--color-border-rgb) / 0.1)',
        },
        tech: {
          cyan:    'rgb(var(--color-accent2) / <alpha-value>)',
          violet:  'rgb(var(--color-accent3) / <alpha-value>)',
          lime:    'rgb(var(--color-success) / <alpha-value>)',
          rose:    'rgb(var(--color-error) / <alpha-value>)',
        }
      },
      borderRadius: {
        '3xl': '1.25rem',
        '4xl': '2rem',
      },
      backgroundImage: {
        'pro-gradient': 'radial-gradient(circle at 50% 50%, #1c1c1e 0%, #000000 100%)',
      }
    },
  },
  plugins: [],
}
