import CircularProgress from "@mui/material/CircularProgress";
import { Stack } from "@mui/material";

export default function Loading() {
    return (
        <Stack
            alignItems="center"
            justifyContent="center"
            sx={{ height: "80vh" }}
        >
            <CircularProgress  size={60} />
        </Stack>
    );
}
