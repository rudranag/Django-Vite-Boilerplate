import { useAxios } from "@/lib/axios";
import { BaseURL } from "@/lib/constants";

export const fetchTodos = async () => {
    const url = `${BaseURL}/api/v1/todo/`;
    const response = await useAxios.get(url);
    return response;
};

interface TodoDataType {
    title: string;
    description: string;
}

export const createTodos = async (todoData: TodoDataType) => {
    const url = `${BaseURL}/api/v1/todo/`;
    const response = await useAxios.post(url, todoData);
    return response;
};

export const updateTodo = async (
    row: TodoDataType & { id: number; completed: boolean }
) => {
    const url = `${BaseURL}/api/v1/todo/${row.id}/`;
    const response = await useAxios.put(url, row);
    return response;
};

export const deleteTodo = async (id: number) => {
    const url = `${BaseURL}/api/v1/todo/${id}/`;
    const response = await useAxios.delete(url);
    return response;
};
