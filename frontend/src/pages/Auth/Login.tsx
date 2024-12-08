import {
    Box,
    Button,
    TextField,
    Typography,
    Container,
    Paper,
} from "@mui/material";

import { useState } from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { login } from "@/api/Auth";
import { useSnackbar } from "@/hooks/useSnackbar";
import { LoginData } from "@/api/Auth";
import { frontEndURL } from "@/lib/constants";

export default function Login() {
    const navigate = useNavigate();
    const location = useLocation();
    const { handleSnackbar } = useSnackbar();
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });

    // Get the 'next' parameter from the URL
    const searchParams = new URLSearchParams(location.search);
    const nextUrl = searchParams.get('next') || '/dashboard';

    const loginMutation = useMutation({
        mutationFn: (data: LoginData) => login({ ...data, next: nextUrl }),
        onSuccess: (response) => {
            handleSnackbar("Logged in successfully", "success");
            // Use the next URL from the response, or fall back to dashboard
            const redirectUrl = response.data.next || '/dashboard';
            // Remove /r prefix if it exists
            const cleanRedirectUrl = redirectUrl.replace(frontEndURL, '/');
            navigate(cleanRedirectUrl);
        },
        onError: (error: any) => {
            handleSnackbar(
                error.response?.data?.detail || "Login failed",
                "error"
            );
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        loginMutation.mutate(formData);
    };

    return (
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    marginTop: 8,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Paper
                    elevation={3}
                    sx={{
                        padding: 4,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        width: "100%",
                    }}
                >
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <Box
                        component="form"
                        onSubmit={handleSubmit}
                        sx={{ mt: 1 }}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Username"
                            name="username"
                            autoComplete="username"
                            autoFocus
                            value={formData.username}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    username: e.target.value,
                                })
                            }
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={formData.password}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    password: e.target.value,
                                })
                            }
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={loginMutation.isPending}
                        >
                            Sign In
                        </Button>
                        <Link
                            to="/signup"
                            style={{
                                textDecoration: "none",
                                color: "inherit",
                            }}
                        >
                            <Typography
                                variant="body2"
                                color="primary"
                                align="center"
                            >
                                Don't have an account? Sign Up
                            </Typography>
                        </Link>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
} 