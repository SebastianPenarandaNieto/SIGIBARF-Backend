from django.urls import path

from apps.usuarios.views import (
    LoginView,
    LogoutView,
    PerfilView,
    RefreshTokenView,
    RegistroView,
)

urlpatterns = [
    path('auth/register/', RegistroView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('me/', PerfilView.as_view(), name='perfil'),
]
