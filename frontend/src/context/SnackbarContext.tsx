import React, { createContext, useState } from "react";
import Box from "@mui/material/Box";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import Alert, { AlertColor, AlertPropsColorOverrides } from '@mui/material/Alert';
import { OverridableStringUnion } from '@mui/types';


interface SnackbarProps {
    handleSnackbar: (message: string, status: StatusType) => void;
    snackbarMessage: string;
    snackbarStatus: StatusType
}

type StatusType = OverridableStringUnion<AlertColor, AlertPropsColorOverrides> | undefined

export const SnackbarContext = createContext<SnackbarProps>({
    handleSnackbar: () => { },
    snackbarMessage: "",
    snackbarStatus: undefined
});


export const SnackbarProvider = ({
    children,
}: {
    children: React.ReactNode;
}) => {
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const [snackbarStatus, setSnackbarStatus] = useState<StatusType>("success");

    const handleSnackbarClose = () => {
        setSnackbarOpen(false);
    };

    const handleSnackbar = (message :string, status: StatusType) => {
        setSnackbarMessage(message);
        setSnackbarOpen(true);
        setSnackbarStatus(status)
    };

    const action = (
        <IconButton
            size="small"
            aria-label="close"
            color="inherit"
            onClick={handleSnackbarClose}
        >
            <CloseIcon fontSize="small" />
        </IconButton>
    );

    return (
        <SnackbarContext.Provider value={{ handleSnackbar, snackbarMessage, snackbarStatus }}>
            {children}
            <Box sx={{ width: 600 }}>
                <Snackbar
                    anchorOrigin={{ vertical: "top", horizontal: "right" }}
                    autoHideDuration={3000}
                    open={snackbarOpen}
                    onClose={handleSnackbarClose}
                    action={action}
                >
                    <Alert
                        onClose={handleSnackbarClose}
                        severity={snackbarStatus}
                        variant="filled"
                        sx={{ width: '100%' }}
                    >
                        {snackbarMessage}
                    </Alert>

                </Snackbar>
            </Box>
        </SnackbarContext.Provider>
    );
};
