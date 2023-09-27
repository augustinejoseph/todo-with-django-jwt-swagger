from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import TodoTask
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from .serializers import UserSerializer, TodoTaskSerializer


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if (
                not username
                or not email
                or not password
                or username is None
                or password is None
                or email is None
            ):
                return Response(
                    {"error": "Username, email, and password are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email is already registered."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            if user:
                return Response(
                    {"message": "Registration successful"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "User authentication failed."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None or not username or not password:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        user.last_login = timezone.now()
        user.save()

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if user is not None:
            user.last_login = timezone.now()
            user.save()

        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
        except TokenError as e:
            return Response(
                {"error": f"Token generation error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_200_OK,
        )


class TodoTaskViewSet(viewsets.ModelViewSet):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
