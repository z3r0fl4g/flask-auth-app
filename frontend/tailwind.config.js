/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Tikepam brand palette from ui_design.md
        amber: {
          100: '#352700', 200: '#6a4e00', 300: '#9f7500', 400: '#d49c00', 500: '#ffbe0b',
          600: '#ffcb3b', 700: '#ffd86c', 800: '#ffe59d', 900: '#fff2ce'
        },
        orange: {
          100: '#331101', 200: '#662202', 300: '#9a3202', 400: '#cd4303', 500: '#fb5607',
          600: '#fc773a', 700: '#fd996b', 800: '#febb9d', 900: '#feddce'
        },
        rose: {
          100: '#330016', 200: '#66002c', 300: '#990042', 400: '#cc0058', 500: '#ff006e',
          600: '#ff338b', 700: '#ff66a8', 800: '#ff99c5', 900: '#ffcce2'
        },
        violet: {
          100: '#190535', 200: '#320a6a', 300: '#4b0fa0', 400: '#6414d5', 500: '#8338ec',
          600: '#9b5ef0', 700: '#b487f4', 800: '#cdaff8', 900: '#e6d7fb'
        },
        azure: {
          100: '#00183e', 200: '#00307c', 300: '#0048bb', 400: '#005ff9', 500: '#3a86ff',
          600: '#609dff', 700: '#88b5ff', 800: '#afceff', 900: '#d7e6ff'
        },
        // Neutrals
        background: '#f8f9ff',
        surface: '#ffffff',
        headline: '#1f2937',
        body: '#4b5563',
        muted: '#9ca3af',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Space Grotesk', 'monospace'],
      },
      fontSize: {
        h1: ['3.125rem', { lineHeight: '1.2' }],
        h2: ['2.25rem', { lineHeight: '1.2' }],
        h3: ['1.5rem', { lineHeight: '1.3' }],
        h4: ['1.25rem', { lineHeight: '1.3' }],
      },
      spacing: {
        'xs': '4px',
        's': '8px',
        'm': '16px',
        'l': '24px',
        'xl': '32px',
        'xxl': '48px',
      },
      borderRadius: {
        '2xl': '16px',
      },
    },
  },
  plugins: [],
}
