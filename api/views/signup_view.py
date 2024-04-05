
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.user_serializer import UserSerializer
from rest_framework import generics
from ..models import User
from rest_framework.permissions import AllowAny

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer