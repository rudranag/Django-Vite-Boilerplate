import axios from "axios";
import { BaseURL } from "./constants";
import { getCookie } from "./utils";
import { defaultUnauthorizedHandler } from "./utils";


export const useAxios = axios.create({
    baseURL: BaseURL,
    timeout: 5000,
    withCredentials: true,
    headers: {
        "X-CSRFToken": getCookie("csrftoken"),
    },
});

// Add a request interceptor
useAxios.interceptors.request.use(
    function (config) {
        // Do something before request is sent
        // console.log(config);

        return config;
    },
    function (error) {
        // Do something with request error
        return Promise.reject(error);
    }
);

// Add a response interceptor
useAxios.interceptors.response.use(
    function (response) {
        return response;
    },
    function (error) {
        if (error.response.status == 403) {
            defaultUnauthorizedHandler()
        }

        return Promise.reject(error);
    }
);
