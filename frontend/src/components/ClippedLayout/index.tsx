import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import { SnackbarProvider } from "@/context/SnackbarContext";
import { Outlet, useNavigate } from "react-router-dom";
import React from "react";
import { mainListItems, secondaryListItems } from "../Sidebar";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { IconButton, Menu, MenuItem, Avatar } from "@mui/material";
import { useMutation } from "@tanstack/react-query";
import { logout } from "@/api/Auth";
import { useSnackbar } from "@/hooks/useSnackbar";

const drawerWidth = 210;

const defaultTheme = createTheme();

export default function ClippedDrawer() {
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const navigate = useNavigate();
    const { handleSnackbar } = useSnackbar();

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const logoutMutation = useMutation({
        mutationFn: logout,
        onSuccess: () => {
            handleSnackbar("Logged out successfully", "success");
            navigate(`/login`);
        },
        onError: () => {
            handleSnackbar("Logout failed", "error");
        },
    });

    const handleLogout = () => {
        logoutMutation.mutate();
        handleClose();
    };

    return (
        <ThemeProvider theme={defaultTheme}>
            <SnackbarProvider>
                <Box sx={{ display: "flex" }}>
                    <CssBaseline />
                    <AppBar
                        position="fixed"
                        sx={{
                            zIndex: (theme) => theme.zIndex.drawer + 1,
                        }}
                    >
                        <Toolbar sx={{ justifyContent: "space-between" }}>
                            <Typography variant="h6" noWrap component="div">
                                React Ninja
                            </Typography>
                            <div>
                                <IconButton
                                    size="large"
                                    aria-label="account of current user"
                                    aria-controls="menu-appbar"
                                    aria-haspopup="true"
                                    onClick={handleMenu}
                                    color="inherit"
                                >
                                    <Avatar sx={{ width: 32, height: 32 }} />
                                </IconButton>
                                <Menu
                                    id="menu-appbar"
                                    anchorEl={anchorEl}
                                    anchorOrigin={{
                                        vertical: "bottom",
                                        horizontal: "right",
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: "top",
                                        horizontal: "right",
                                    }}
                                    open={Boolean(anchorEl)}
                                    onClose={handleClose}
                                >
                                    <MenuItem onClick={handleClose}>
                                        Profile
                                    </MenuItem>
                                    <MenuItem onClick={handleLogout}>
                                        Logout
                                    </MenuItem>
                                </Menu>
                            </div>
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
                            <List component="nav">
                                {mainListItems}
                                <Divider sx={{ my: 1 }} />
                                {secondaryListItems}
                            </List>
                        </Box>
                    </Drawer>
                    <Box
                        component="main"
                        sx={{
                            flexGrow: 1,
                            p: 3,
                            width: `calc(100% - ${drawerWidth}px)`,
                        }}
                    >
                        <Toolbar />
                        <Outlet />
                    </Box>
                </Box>
            </SnackbarProvider>
        </ThemeProvider>
    );
}
