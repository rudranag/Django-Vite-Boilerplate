/// <reference types="vitest" />

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    root: "./src",
    server: {
        host: "127.0.0.1",
        port: 9900,
    },
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    build: {
        manifest: true,
        outDir: "../dist",
        emptyOutDir: true,
    },
    base: process.env.NODE_ENV === "production" ? "/static/" : "/",
    test: {
        globals: true,
        css: true,
        environment: "jsdom",
        setupFiles: ["./vitest.setup.ts"],
        coverage: {
            provider: 'v8',
            reporter: ['lcov'],
            // reporter: ['text', 'json', 'html', 'cobertura'],
            reportsDirectory: '../../coverage/frontend/',
          },
    },
});
