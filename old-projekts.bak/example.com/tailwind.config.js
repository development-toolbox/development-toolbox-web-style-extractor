/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./pages/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./public/**/*.html"
  ],
  theme: {
    extend: {
      "colors": {
        "primary": "#fdfdff",
        "secondary": "#f0f0f2",
        "accent": "#38488f",
        "background": "#ffffff",
        "extracted": {
          "extracted-1": "#fdfdff",
          "extracted-2": "#f0f0f2",
          "extracted-3": "#38488f"
        }
      },
      "fontFamily": {
        "primary": [
          "Segoe UI",
          "system-ui",
          "sans-serif"
        ],
        "secondary": [
          "Helvetica Neue",
          "system-ui",
          "sans-serif"
        ],
        "display": [
          "system-ui",
          "system-ui",
          "sans-serif"
        ]
      },
      "spacing": {
        "18": "4.5rem",
        "88": "22rem",
        "112": "28rem",
        "128": "32rem"
      },
      "borderRadius": {
        "4xl": "2rem",
        "5xl": "2.5rem"
      },
      "boxShadow": {
        "soft": "0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)",
        "brand": "0 4px 14px 0 #fdfdff40"
      }
    }
  },
  plugins: []
}

/*
Usage Examples:

1. In your HTML/JSX:
   <div className="bg-primary text-white font-primary">
     Primary styled content
   </div>
   
   <div className="bg-extracted-1 text-secondary font-secondary">
     Using extracted colors and fonts
   </div>

2. Custom utility classes:
   <div className="shadow-soft rounded-4xl p-18">
     Custom spacing and shadows
   </div>
   
3. Responsive design:
   <div className="bg-primary md:bg-secondary lg:bg-accent">
     Responsive background colors
   </div>

4. Dark mode (if enabled):
   <div className="bg-primary dark:bg-secondary">
     Dark mode support
   </div>
*/