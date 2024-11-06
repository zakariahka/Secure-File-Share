import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'light-pink-orange': '#ffad99',
        'pink-orange': '#ff8466',
        'dark-pink-orange': '#ff704d',
        'words-pink-orange': '#ff704d'
      },
    },
  },
  plugins: [],
};
export default config;
