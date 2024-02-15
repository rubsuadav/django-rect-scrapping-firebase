/// <reference types="cypress" />

describe("rendering App component", () => {
  it("should render the app", () => {
    cy.visit("http://localhost:5173/");
    cy.get("span").contains("Inicio");
  });
});
