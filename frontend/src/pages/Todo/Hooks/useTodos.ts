// useTodoMutations.js
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createTodos, deleteTodo, updateTodo } from "@/api/Todos";
import { useSnackbar } from "@/hooks/useSnackbar";

export const useTodoMutations = () => {
    const { handleSnackbar } = useSnackbar();
    const queryClient = useQueryClient();

    // Create Todo Mutation
    const createTodoMutation = useMutation({
        mutationFn: createTodos,
        onSuccess: (res) => {
            if (res.status === 201) {
                queryClient.invalidateQueries({ queryKey: ["todos"] });
                handleSnackbar("Added new todo", "success");
            }
        },
        onError: (res) => {
            console.log(res);
            queryClient.invalidateQueries({ queryKey: ["todos"] });
            handleSnackbar("Failed to add todo", "warning");
        },
    });

    // Delete Todo Mutation
    const deleteTodoMutation = useMutation({
        mutationFn: deleteTodo,
        onSuccess: (res) => {
            if (res.status === 204) {
                handleSnackbar("Todo has been deleted", "success");
            }
        },
        onError: (res) => {
            console.log(res);
            queryClient.invalidateQueries({ queryKey: ["todos"] });
            handleSnackbar("Failed to delete todo", "warning");
        },
    });

    const updateTodoMutation = useMutation({
        mutationFn: updateTodo,
        onSuccess: (res) => {
            if (res.status === 200) {
                handleSnackbar("Todo has been updated", "success");
            }
        },
        onError: (res) => {
            console.log(res);
            queryClient.invalidateQueries({ queryKey: ["todos"] });
            handleSnackbar("Failed to update todo", "warning");
        },
    });

    return {
        createTodoMutation,
        deleteTodoMutation,
        updateTodoMutation,
    };
};
