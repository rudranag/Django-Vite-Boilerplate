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
            expect(within(list).getAllByRole("listitem")).toHaveLength(4);
            expect(within(list).getAllByRole("link")).toHaveLength(4);
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
            const list = screen.getByRole("list");
            const cases: Array<{ name: RegExp; href: string }> = [
                { name: /dashboard/i, href: "/dashboard" },
                { name: /orders/i, href: "/orders" },
                { name: /customers/i, href: "/" },
                { name: /todos/i, href: "/todo" },
            ];
            cases.forEach(({ name, href }) => {
                const link = within(list).getByRole("link", { name });
                expect(link).toHaveAttribute("href", href);
            });
        });
    });
});
