import * as React from "react";
import Box from "@mui/material/Box";
import {
    GridRowModesModel,
    GridRowModes,
    DataGrid, GridEventListener,
    GridRowId, GridRowEditStopReasons,
    GridSlots
} from "@mui/x-data-grid";

import { useQuery } from "@tanstack/react-query";

import { fetchTodos } from "@/api/Todos";
import { useTodoMutations } from "@/pages/Todo/Hooks/useTodos";
import Loading from "@/components/Loading";
import EditToolbar from "@/pages/Todo/components/EditToolbar";
import { TodoColumns } from "./components/TodoColumns";

interface Todo {
    id: number;
    title: string;
    description: string;
    created_at: string;
    completed: boolean;
    isNew?: boolean;
}

type NewTodo = Todo & { isNew?: boolean };

export default function Todo() {
    const [rows, setRows] = React.useState<Todo[]>([]);
    const [rowModesModel, setRowModesModel] = React.useState<GridRowModesModel>({});
    const { createTodoMutation, deleteTodoMutation, updateTodoMutation } = useTodoMutations();

    const { data, isLoading, isError } = useQuery({
        queryKey: ["todos"],
        queryFn: fetchTodos,
    });


    React.useEffect(() => {
        if (data) {
            setRows(data.data);
        }
    }, [data]);


    const handleRowEditStop: GridEventListener<"rowEditStop"> = (
        params,
        event
    ) => {
        if (params.reason === GridRowEditStopReasons.rowFocusOut) {
            event.defaultMuiPrevented = true;
        }
    };

    const handleEditClick = (id: GridRowId) => () => {
        setRowModesModel({
            ...rowModesModel,
            [id]: { mode: GridRowModes.Edit },
        });
    };

    const handleSaveClick = (id: GridRowId) => () => {
        setRowModesModel({
            ...rowModesModel,
            [id]: { mode: GridRowModes.View },
        });
    };

    const handleDeleteClick = (id: GridRowId) => () => {
        setRows(rows.filter((row) => row.id !== id));
        deleteTodoMutation.mutate(id as number);
    };

    const handleCancelClick = (id: GridRowId) => () => {
        setRowModesModel({
            ...rowModesModel,
            [id]: { mode: GridRowModes.View, ignoreModifications: true },
        });

        const editedRow = rows.find((row) => row.id === id);
        if (editedRow!.isNew) {
            setRows(rows.filter((row) => row.id !== id));
        }
    };

    const processRowUpdate = (newRow: NewTodo) => {
        // Remove `isNew` property when processing the row
        const { isNew, ...todoData } = newRow;

        // Create new todo if `isNew` is true
        if (isNew) {
            createTodoMutation.mutate(todoData);
        } else {
            updateTodoMutation.mutate(todoData);
        }

        const updatedRow: Todo = { ...todoData };

        setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));

        return updatedRow;
    };

    const handleRowModesModelChange = (newRowModesModel: GridRowModesModel) => {
        setRowModesModel(newRowModesModel);
    };


    if (isLoading) return <Loading />;
    if (isError) return <div>Error fetching todos</div>;

    return (
            <Box
                sx={{
                    height: 500,
                    width: "100%",
                    "& .actions": {
                        color: "text.secondary",
                    },
                    "& .textPrimary": {
                        color: "text.primary",
                    },
                }}
            >
                <DataGrid
                    rows={rows}
                    columns={TodoColumns({
                        rowModesModel,
                        handleEditClick,
                        handleSaveClick,
                        handleCancelClick,
                        handleDeleteClick,
                    })}
                    editMode="row"
                    rowModesModel={rowModesModel}
                    onRowModesModelChange={handleRowModesModelChange}
                    onRowEditStop={handleRowEditStop}
                    processRowUpdate={processRowUpdate}
                    slots={{
                        toolbar: EditToolbar as GridSlots["toolbar"],
                    }}
                    slotProps={{
                        toolbar: { setRows, setRowModesModel },
                    }}
                    initialState={{
                        columns: {
                            columnVisibilityModel: {
                                // Hide id column, the other columns will remain visible
                                id: false,
                            },
                        },
                    }}
                />
            </Box>
    );
}
