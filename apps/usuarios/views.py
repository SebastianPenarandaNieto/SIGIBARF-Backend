from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.usuarios.permissions import get_user_role_name
from apps.usuarios.serializers import LoginSerializer, RegistroSerializer, UsuarioSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    rol = get_user_role_name(user)
    if rol:
        refresh['rol'] = rol
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'tokens': get_tokens_for_user(user),
                'user': UsuarioSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(
            {
                'tokens': get_tokens_for_user(user),
                'user': UsuarioSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response(
                {'detail': 'Se requiere el campo refresh.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            return Response(
                {'detail': 'Refresh token inválido o ya revocado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        completo = bool(user.telefono.strip() and user.direccion.strip())
        if user.is_perfil_completo != completo:
            user.is_perfil_completo = completo
            user.save(update_fields=['is_perfil_completo'])


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]
