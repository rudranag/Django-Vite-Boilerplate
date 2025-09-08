from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from ninja import NinjaAPI
from apps.todos.api import api as todos_api
from apps.contacts.api import api as contacts_api
from apps.organizations.api import api as organizations_api

api = NinjaAPI(csrf=True)
api.add_router("/todos", todos_api)
api.add_router("/contacts", contacts_api)
api.add_router("/organizations", organizations_api)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include("apps.users.urls")),
    path("api/v1/", api.urls),
]

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

urlpatterns += [path('', include("apps.vite_integration.urls"))]