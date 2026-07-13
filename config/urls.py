from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView
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
    path('api/schema/', SpectacularJSONAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(), name='docs'),
]