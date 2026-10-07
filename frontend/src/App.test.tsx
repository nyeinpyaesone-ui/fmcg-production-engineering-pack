import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("renders the scaffold heading", () => {
    render(<App />);
    const heading = screen.getByRole("heading", { name: /scaffold/i });
    expect(heading).toBeInTheDocument();
    expect(heading).toBeVisible();
  });
});
