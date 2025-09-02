import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { mainListItems } from ".";
import { MemoryRouter } from "react-router-dom";
import { List } from "@mui/material";

describe("Sidebar", () => {
    describe("mainListItems", () => {
        it("should render the main list items", () => {
            render(
                <MemoryRouter>
                    <List>{mainListItems}</List>
                </MemoryRouter>
            );
            const list = screen.getByRole("list");
            const listItems = within(list).getAllByRole("link");
            expect(listItems).toHaveLength(4);
            expect(screen.getByText("Dashboard")).toBeInTheDocument();
            expect(screen.getByText("Orders")).toBeInTheDocument();
            expect(screen.getByText("Customers")).toBeInTheDocument();
            expect(screen.getByText("Todos")).toBeInTheDocument();
        });

        it("should have the correct links", () => {
            render(
                <MemoryRouter>
                    <List>{mainListItems}</List>
                </MemoryRouter>
            );
            const dashboardLink = screen.getByRole("link", { name: /dashboard/i });
            expect(dashboardLink).toHaveAttribute("href", "/dashboard");

            const ordersLink = screen.getByRole("link", { name: /orders/i });
            expect(ordersLink).toHaveAttribute("href", "/orders");

            const customersLink = screen.getByRole("link", { name: /customers/i });
            expect(customersLink).toHaveAttribute("href", "/");

            const todosLink = screen.getByRole("link", { name: /todos/i });
            expect(todosLink).toHaveAttribute("href", "/todo");
        });
    });
});
