import { defineConfig } from "vite";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },

  server: {
    port: 3000,
    proxy: {
      // send auth + API calls to Flask @ 5000, avoids CORS in dev
      "/auth": { target: "http://127.0.0.1:5000", changeOrigin: true },
      "/me": { target: "http://127.0.0.1:5000", changeOrigin: true },
      "/logout": { target: "http://127.0.0.1:5000", changeOrigin: true },
    },
  },
});
