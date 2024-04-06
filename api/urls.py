from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.signup_view import SignUpView
from .views.user_search_view import UserSearchView
from .views.friend_request_view import FriendRequestListAPIView, FriendRequestDetailAPIView
from .views.friend_view import ListFriendsAPI


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('search/<str:search_keyword>/', UserSearchView.as_view(), name='user_search'),
    path('friend-requests/', FriendRequestListAPIView.as_view(), name='friend_requests'),
    path('friend-requests/<int:request_id>/', FriendRequestDetailAPIView.as_view(), name='friend_request_detail'),
    path('friends/',ListFriendsAPI.as_view(), name="friend")
]
