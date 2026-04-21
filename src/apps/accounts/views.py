from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsAllowedAction
from drf_spectacular.utils import extend_schema

from apps.accounts.serializers import RegisterSerializer, LoginSerializer, ProfileUpdateSerializer
from apps.accounts.services import register_user, authenticate_user, logout_user, soft_delete_user
from utils.tokens import authenticate_token

class RegisterView(APIView):
    @extend_schema(request=RegisterSerializer, responses={201: {"token": "string", "user_id": "int"}})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.pop('password2')
        
        user = register_user(**data)
        token_obj = authenticate_user(user.email, data['password'])
        return Response({"token": token_obj["token"], "user_id": user.id}, status=201)

class LoginView(APIView):
    @extend_schema(request=LoginSerializer, responses={200: {"token": "string"}})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = authenticate_user(**serializer.validated_data)
        return Response(result, status=200)

class LogoutView(APIView):
    permission_classes = [IsAllowedAction]
    def post(self, request):
        # Токен берём из заголовка, который установил middleware
        logout_user(request.auth.key)
        return Response(status=204)

class ProfileView(APIView):
    permission_classes = [IsAllowedAction]
    
    def get(self, request):
        serializer = ProfileUpdateSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request):
        soft_delete_user(request.user)
        return Response(status=204)