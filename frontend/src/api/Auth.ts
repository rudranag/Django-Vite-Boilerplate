import { useAxios } from "@/lib/axios";
import { BaseURL } from "@/lib/constants";

export interface LoginData {
    username: string;
    password: string;
    next?: string;
}

interface SignupData extends LoginData {
    email: string;
    password2: string;
}

export const login = async (data: LoginData) => {
    const url = `${BaseURL}/api/v1/auth/login/`;
    const response = await useAxios.post(url, data);
    return response;
};

export const signup = async (data: SignupData) => {
    const url = `${BaseURL}/api/v1/auth/signup/`;
    const response = await useAxios.post(url, data);
    return response;
};

export const logout = async () => {
    const url = `${BaseURL}/api/v1/auth/logout/`;
    const response = await useAxios.post(url);
    return response;
}; 