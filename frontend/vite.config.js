import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: "happy-dom",
    browser: {
      enabled: true,
      name: "chrome",
    },
    coverage: {
      provider: "istanbul",
      reporter: ["text", "html", "json-summary", "lcovonly"],
    },
  },
});
