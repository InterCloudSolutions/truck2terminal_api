# Create your views here.

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_token_from_request(self, request):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return request.query_params.get("token", None)

    def post(self, request):
        token = self.get_token_from_request(request)
        if not token:
            return Response(
                {"detail": "No token provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        jwt_auth = JWTAuthentication()
        try:
            decoded_token = jwt_auth.get_validated_token(token)
        except (IndexError, InvalidToken):
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            user = User.objects.get(id=decoded_token["user_id"])
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Use f-string for full name concatenation
        full_name = f"{user.first_name} {user.last_name}"

        user_info = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": full_name,
            "last_login": user.last_login,
        }

        response_data = {
            "user": user_info,
            "access": token,
            "exp": decoded_token["exp"],
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only Admin can CRUD users

    def get_queryset(self):
        role = self.request.query_params.get("role")
        if role:
            return self.queryset.filter(role=role)
        return self.queryset
