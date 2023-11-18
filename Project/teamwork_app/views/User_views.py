from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from teamwork_app.models import POSITION_CHOICES
from teamwork_app.serializers import EmployeeSerializer, EmployeeSerializerAuth
from teamwork_app.tokens import create_jwt_pair_for_user


class RegisterView(APIView, TemplateView):
    """
    Регистрация пользователей
    """
    template_name = 'registration.html'
    permission_classes = []
    serializer_class = EmployeeSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        positions = dict(POSITION_CHOICES)
        context['positions'] = positions
        return context

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                validate_password(request.data["password"])
            except Exception as password_errors:
                errors = []
                for error in password_errors:
                    errors.append(error)
                response = {
                    "Status": False,
                    "Errors": errors
                }
                return Response(data=response, status=HTTP_400_BAD_REQUEST)

            serializer.save()
            response = {
                "message": "User created successfully",
                "data": serializer.data
            }
            return Response(data=response, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class AuthView(APIView, TemplateView):
    """
    Авторизация пользователей
    """
    template_name = "auth.html"
    permission_classes = []
    serializer_class = EmployeeSerializerAuth

    def post(self, request: Request) -> Response:
        email = request.data["email"]
        password = request.data["password"]

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message": "Login successfully",
                "tokens": tokens
            }
            return Response(data=response, status=HTTP_200_OK)
        else:
            response = {
                "Status": False,
                "message": "Invalid email or password"
            }
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
