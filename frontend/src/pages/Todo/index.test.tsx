import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DataGrid, GridRowModesModel, GridRowModes } from "@mui/x-data-grid";
import { TodoColumns } from "@/pages/Todo/components/TodoColumns";

describe("TodoColumns component", () => {
    it("should render Save and Cancel buttons when in edit mode", () => {
        const rowModesModel: GridRowModesModel = {
            1: { mode: GridRowModes.Edit },
        };

        const handleEditClick = vi.fn();
        const handleSaveClick = vi.fn();
        const handleCancelClick = vi.fn();
        const handleDeleteClick = vi.fn();

        const columns = TodoColumns({
            rowModesModel,
            handleEditClick,
            handleSaveClick,
            handleCancelClick,
            handleDeleteClick,
        });

        render(
            <DataGrid
                rows={[{ id: 1, title: "Test Todo" }]}
                columns={columns}
                rowModesModel={rowModesModel}
            />
        );

        // Check for Save and Cancel buttons in edit mode
        expect(screen.getByLabelText("Save")).toBeInTheDocument();
        expect(screen.getByLabelText("Cancel")).toBeInTheDocument();
    });

    it("should render Edit and Delete buttons when not in edit mode", () => {
        const rowModesModel: GridRowModesModel = {
            1: { mode: GridRowModes.View },
        };

        const handleEditClick = vi.fn();
        const handleSaveClick = vi.fn();
        const handleCancelClick = vi.fn();
        const handleDeleteClick = vi.fn();

        const columns = TodoColumns({
            rowModesModel,
            handleEditClick,
            handleSaveClick,
            handleCancelClick,
            handleDeleteClick,
        });

        render(
            <DataGrid
                rows={[{ id: 1, title: "Test Todo" }]}
                columns={columns}
                rowModesModel={rowModesModel}
            />
        );

        // Check for Edit and Delete buttons in view mode
        expect(screen.getByLabelText("Edit")).toBeInTheDocument();
        expect(screen.getByLabelText("Delete")).toBeInTheDocument();
    });
});
