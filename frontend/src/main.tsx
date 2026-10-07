import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { ErrorBoundary } from "./ErrorBoundary";

const el = document.getElementById("root");
if (el === null) {
  document.body.textContent = "Application root is missing.";
} else {
  createRoot(el).render(
    <StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </StrictMode>,
  );
}
