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
        "primary": "#ffffffcc",
        "secondary": "#ffffffb3",
        "accent": "#ffffff66",
        "background": "#ffffff",
        "extracted": {
          "extracted-1": "#ffffffcc",
          "extracted-2": "#ffffffb3",
          "extracted-3": "#ffffff66",
          "extracted-4": "#ffffff33",
          "extracted-5": "#ffffff26",
          "extracted-6": "#ffffff1a",
          "extracted-7": "#ffffff00",
          "extracted-8": "#fff8c5",
          "extracted-9": "#fff2d5",
          "extracted-10": "#fff1e5"
        }
      },
      "fontFamily": {},
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
        "brand": "0 4px 14px 0 #ffffffcc40"
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