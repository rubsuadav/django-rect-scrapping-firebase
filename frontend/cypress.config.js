import { defineConfig } from "cypress";
import vitePreprocessor from "cypress-vite";
import codeCoverageTask from "@cypress/code-coverage/task.js";

export default defineConfig({
  projectId: "gsxmt1",
  reporter: "mochawesome",
  e2e: {
    setupNodeEvents(on, config) {
      codeCoverageTask(on, config);
      on("file:preprocessor", vitePreprocessor());
      return config;
    },
  },
});
