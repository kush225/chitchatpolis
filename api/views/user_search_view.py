from rest_framework import generics, status
from rest_framework.response import Response
from ..models import User
from ..serializers.user_serializer import UserSerializer
from ..serializers.user_search_serializer import UserSearchSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class UserSearchView(generics.ListAPIView):
    """
    API view to search users by email or name.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Get the queryset of users filtered by search keyword.
        """
        # Initialize the queryset with all users
        queryset = self.queryset

        # Initialize search keyword as None
        search_keyword = None

        # Check if search keyword is provided in URL kwargs
        if 'search_keyword' in self.kwargs:
            # Create a search serializer instance
            search_serializer = UserSearchSerializer(data=self.kwargs)

            # Check if search serializer is valid
            if search_serializer.is_valid(raise_exception=False):
                # Extract the validated search keyword
                search_keyword = search_serializer.validated_data.get('search_keyword')

        # If search keyword is provided and valid
        if search_keyword:
            # Filter users by exact email match
            exact_email_match = queryset.filter(email=search_keyword)

            # If exact email match exists, return it
            if exact_email_match.exists():
                logger.info(f"Exact email match found for search keyword: {search_keyword}")
                return exact_email_match

            # If no exact email match, filter users by name containing the search keyword
            logger.info(f"No exact email match found for search keyword: {search_keyword}. Filtering by name.")
            return queryset.filter(name__icontains=search_keyword)

        # If no search keyword provided or not valid, return all users
        return queryset
