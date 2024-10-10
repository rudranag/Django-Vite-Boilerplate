import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/DeleteOutlined";
import SaveIcon from "@mui/icons-material/Save";
import CancelIcon from "@mui/icons-material/Close";
import {
    GridColDef,
    GridActionsCellItem,
    GridRowId,
    GridRowModesModel,
    GridRowModes,
} from "@mui/x-data-grid";
import dayjs from "dayjs";

interface TodoColumnsProps {
    rowModesModel: GridRowModesModel;
    handleEditClick: (id: GridRowId) => () => void;
    handleSaveClick: (id: GridRowId) => () => void;
    handleCancelClick: (id: GridRowId) => () => void;
    handleDeleteClick: (id: GridRowId) => () => void;
}

export const TodoColumns = ({
    rowModesModel,
    handleEditClick,
    handleSaveClick,
    handleCancelClick,
    handleDeleteClick,
}: TodoColumnsProps): GridColDef[] => {
    return [
        { field: "id", headerName: "ID", flex: 1, minWidth: 70 },
        {
            field: "title",
            headerName: "Title",
            flex: 2,
            minWidth: 150,
            editable: true,
        },
        {
            field: "description",
            headerName: "Description",
            flex: 3,
            minWidth: 330,
            editable: true,
        },
        {
            field: "created_at",
            headerName: "Created At",
            type: "dateTime",
            flex: 2,
            minWidth: 160,
            valueGetter: (value) => new Date(value),
            valueFormatter: (value) =>
                dayjs(value).format("DD/MM/YYYY hh:mm A"),
        },
        {
            field: "completed",
            headerName: "Completed",
            type: "boolean",
            flex: 1,
            minWidth: 100,
            editable: true,
        },
        {
            field: "actions",
            type: "actions",
            headerName: "Actions",
            width: 100,
            cellClassName: "actions",
            getActions: ({ id }) => {
                const isInEditMode =
                    rowModesModel[id]?.mode === GridRowModes.Edit;

                if (isInEditMode) {
                    return [
                        <GridActionsCellItem
                            icon={<SaveIcon />}
                            label="Save"
                            sx={{ color: "primary.main" }}
                            onClick={handleSaveClick(id)}
                        />,
                        <GridActionsCellItem
                            icon={<CancelIcon />}
                            label="Cancel"
                            className="textPrimary"
                            onClick={handleCancelClick(id)}
                            color="inherit"
                        />,
                    ];
                }

                return [
                    <GridActionsCellItem
                        icon={<EditIcon />}
                        label="Edit"
                        className="textPrimary"
                        onClick={handleEditClick(id)}
                        color="inherit"
                    />,
                    <GridActionsCellItem
                        icon={<DeleteIcon />}
                        label="Delete"
                        onClick={handleDeleteClick(id)}
                        color="inherit"
                    />,
                ];
            },
        },
    ];
};
