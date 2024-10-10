from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Django Todos",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.rudranag.com/policies/terms/",
        contact=openapi.Contact(email="contact@rudranag.com"),
        license=openapi.License(name="Apache 2.0 License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
