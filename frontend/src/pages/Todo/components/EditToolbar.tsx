import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import {
    GridRowsProp,
    GridRowModesModel,
    GridRowModes,
    GridToolbarContainer,
} from "@mui/x-data-grid";
import { randomId } from "@mui/x-data-grid-generator";

interface EditToolbarProps {
    setRows: (newRows: (oldRows: GridRowsProp) => GridRowsProp) => void;
    setRowModesModel: (
        newModel: (oldModel: GridRowModesModel) => GridRowModesModel
    ) => void;
}

export default function EditToolbar(props: EditToolbarProps) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            {
                id,
                title: "",
                description: "",
                created_at: new Date(),
                isNew: true,
            },
        ]);

        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: "title" },
        }));
    };

    return (
        <GridToolbarContainer>
            <Button
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleClick}
            >
                Add Todo
            </Button>
        </GridToolbarContainer>
    );
}
