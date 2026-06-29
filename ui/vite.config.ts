import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Config-driven API base URL is read at runtime from import.meta.env.VITE_API_BASE.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
  },
  preview: {
    port: 3000,
    host: true,
  },
});
