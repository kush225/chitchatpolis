from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..serializers.user_serializer import UserSerializer
from ..models import User
import logging

logger = logging.getLogger(__name__)

class SignUpView(generics.CreateAPIView):
    """
    API view to handle user signup.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Perform user creation and log the event.
        """
        logger.info(f"User signed up with email: {serializer.validated_data['email']}")
        serializer.save()

