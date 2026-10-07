import { Component, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
}

/** Last-resort error containment: one throw must never blank the page silently. */
export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  render(): ReactNode {
    if (this.state.error !== null) {
      return (
        <main>
          <h1>Something went wrong</h1>
          <p>Reload the page. If the problem persists, contact support.</p>
        </main>
      );
    }
    return this.props.children;
  }
}
