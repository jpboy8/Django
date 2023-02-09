from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi


schema_view = get_schema_view(  # new
    openapi.Info(
        title="Bank API",
        default_version="v1",
        description="A sample API for bank app",
        contact=openapi.Contact(email="qwerty@example.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
