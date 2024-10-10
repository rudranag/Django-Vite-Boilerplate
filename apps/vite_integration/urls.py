
from django.contrib import admin
from django.urls import re_path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # must be at last to catch all non existing routes
    # re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(
        r"^r/.*$",
        login_required(TemplateView.as_view(template_name="react_base.html"))
    ),
   
]



admin.site.site_header = "React Ninja Vite"
admin.site.site_title = "React Ninja Vite Portal"
admin.site.index_title = "Welcome to the React Ninja Portal" 