from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("", include("ui.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("api/auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("api/auth/jwt/logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path('apischema/', get_schema_view(title="Identity Management API",
         description="API for managing identities and relationships",
         version="1.0.0"), name='openapi-schema'),
    path('swagger-docs/', TemplateView.as_view(
         template_name='ui/swagger-docs.html',
         extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
]