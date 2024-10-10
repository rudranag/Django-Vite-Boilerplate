import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import OutlinedInput from "@mui/material/OutlinedInput";
import { useState, ChangeEvent } from "react";
import Grid from "@mui/material/Unstable_Grid2";
import Box from "@mui/material/Box";

interface User {
    firstName: string;
    lastName: string;
    email: string;
    address: string;
}

export default function UserForm() {
    const [user, setUser] = useState<User>({
        firstName: "",
        lastName: "",
        email: "",
        address: "",
    });

    const handleChange = (
        e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
    ) => {
        setUser({
            ...user,
            [e.target.name]: e.target.value,
        });
        console.log(user, "user");
    };
    return (
            <Box
                component="form"
                sx={{ flexGrow: 1, m: 4 }}
                noValidate
                autoComplete="off"
            >
                <Grid
                    container
                    spacing={{ xs: 2, md: 3 }}
                    columns={{ xs: 4, sm: 8, md: 12 }}
                >
                    <Grid xs={12} sm={4} md={3}>
                        <FormControl fullWidth={true}>
                            <InputLabel htmlFor="component-outlined">
                                First Name
                            </InputLabel>
                            <OutlinedInput
                                id="component-first"
                                className="MuiOutlinedInput-sizeSmall"
                                label="First Name"
                                name="firstName"
                                onChange={handleChange}
                                value={user.firstName}
                            />
                        </FormControl>
                    </Grid>

                    <Grid xs={12} sm={4} md={3}>
                        <FormControl fullWidth={true}>
                            <InputLabel htmlFor="component-outlined">
                                Last Name
                            </InputLabel>
                            <OutlinedInput
                                id="component-last"
                                className="MuiOutlinedInput-sizeSmall"
                                label="Last Name"
                                name="lastName"
                                onChange={handleChange}
                                value={user.lastName}
                            />
                        </FormControl>
                    </Grid>

                    <Grid xs={12} sm={4} md={3}>
                        <FormControl fullWidth={true}>
                            <InputLabel htmlFor="component-outlined">
                                Email
                            </InputLabel>
                            <OutlinedInput
                                id="component-email"
                                label="Email"
                                name="email"
                                onChange={handleChange}
                                value={user.email}
                            />
                        </FormControl>
                    </Grid>

                    <Grid xs={12} sm={4} md={3}>
                        <FormControl fullWidth={true}>
                            <InputLabel htmlFor="component-outlined">
                                Address
                            </InputLabel>
                            <OutlinedInput
                                id="component-address"
                                label="Address"
                                name="address"
                                onChange={handleChange}
                                value={user.address}
                            />
                        </FormControl>
                    </Grid>
                </Grid>

                <Box textAlign={"center"} sx={{ m: 3 }}>
                    <Button variant="contained">Submit</Button>
                </Box>
            </Box>
    );
}
