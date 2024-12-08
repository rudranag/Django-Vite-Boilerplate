from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include("apps.users.urls")),
    path('api/v1/', include("apps.todos.urls")),
    path('swagger/', include("apps.swagger.urls")),
]

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

urlpatterns += [path('', include("apps.vite_integration.urls"))]