from django.urls import path
from apps.todos.api import TodoListCreateView,TodoRetrieveUpdateDestroyView

urlpatterns = [
    path('v1/todo/',TodoListCreateView.as_view(),name="todo-list-create"),
    path('v1/todo/<int:id>/', TodoRetrieveUpdateDestroyView.as_view(),name="todo-detail"),
]
