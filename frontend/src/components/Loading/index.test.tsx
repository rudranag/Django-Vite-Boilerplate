import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Loading from ".";

describe("Loading", () => {
    it("should render", () => {
        render(<Loading />);
        expect(screen.getByRole("progressbar")).toBeInTheDocument();
        expect(screen.getAllByRole("progressbar")).toHaveLength(1);
    });
});
