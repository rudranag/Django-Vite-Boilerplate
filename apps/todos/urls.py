from django.urls import path
from apps.todos.api import TodoListCreateView, TodoRetrieveUpdateDestroyView

urlpatterns = [
    path('todo/', TodoListCreateView.as_view(), name="todo-list-create"),
    path('todo/<int:id>/', TodoRetrieveUpdateDestroyView.as_view(), name="todo-detail"),
]
