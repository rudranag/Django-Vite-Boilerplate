import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import { SnackbarProvider } from "@/context/SnackbarContext";
import { Outlet } from "react-router-dom";
import React from "react";
import { mainListItems, secondaryListItems } from "../Sidebar";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const drawerWidth = 210;

const defaultTheme = createTheme();
export default function ClippedDrawer() {
    return (
        <ThemeProvider theme={defaultTheme}>
            <Box sx={{ display: "flex" }}>
                <CssBaseline />
                <AppBar
                    position="fixed"
                    sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
                >
                    <Toolbar>
                        <Typography variant="h6" noWrap component="div">
                            Clipped drawer
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Drawer
                    variant="permanent"
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        [`& .MuiDrawer-paper`]: {
                            width: drawerWidth,
                            boxSizing: "border-box",
                        },
                    }}
                >
                    <Toolbar />
                    <Box sx={{ overflow: "auto" }}>
                        <Divider />
                        <List component="nav">
                            {mainListItems}
                            <Divider sx={{ my: 1 }} />
                            {secondaryListItems}
                        </List>
                        <Divider />
                    </Box>
                </Drawer>
                <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                    <Toolbar />
                    <SnackbarProvider>
                        <React.Suspense>
                            <Outlet />
                        </React.Suspense>
                    </SnackbarProvider>
                </Box>
            </Box>
        </ThemeProvider>
    );
}
