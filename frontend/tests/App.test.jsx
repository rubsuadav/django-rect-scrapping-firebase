import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import App from "../src/App";

describe("App", () => {
  afterEach(() => {
    cleanup();
  });

  it("should render", () => {
    render(<App />);
    expect(screen.getByText("Inicio")).toBeTruthy();
  });
});
