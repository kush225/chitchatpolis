from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..serializers.user_serializer import UserSerializer
from ..models import User

class SignUpView(generics.CreateAPIView):
    """
    API view to handle user signup.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer