from django.contrib import admin
from apps.todos.models import Todo

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ["id",'title',"user","completed"]
    readonly_fields = ["created_at"]
    list_display_links = ("title",)

admin.site.register(Todo,TodoAdmin)