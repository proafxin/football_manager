"""Define views for exposing API endpoints"""


from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions

from manager import models, serializers

UserModel = get_user_model()
AUTHENTICATIONS = [
    authentication.BasicAuthentication,
    authentication.SessionAuthentication,
    authentication.TokenAuthentication,
]

PERMISSIONS: list = [permissions.IsAuthenticated]


class UserRegisterView(generics.CreateAPIView):
    """
    Register using email and password
    """

    model = UserModel
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserSerializer


class ManagerListView(generics.ListAPIView):
    """View managers of current user"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = AUTHENTICATIONS
    serializer_class = serializers.ManagerSerializer

    def get_queryset(self):
        return models.Manager.objects.filter(user=self.request.user)


class AttributeCategoryListView(generics.ListCreateAPIView):
    """Get, Post, Put, Delete API for AttributeCategory"""

    queryset = models.AttributeCategory.objects.all()
    serializer_class: serializers.AttributeCategorySerializer = (
        serializers.AttributeCategorySerializer
    )
    authentication_classes = AUTHENTICATIONS
    permission_classes = [permissions.IsAdminUser]


class CountryListView(generics.ListCreateAPIView):
    """Get, Post, Put, Delete API for Country"""

    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    authentication_classes = AUTHENTICATIONS
    permission_classes = [permissions.IsAdminUser]


class LeagueListView(generics.ListCreateAPIView):
    """Get, Post, Put, Delete API for League"""

    queryset = models.League.objects.all()
    serializer_class = serializers.LeagueSerializer
    authentication_classes = AUTHENTICATIONS
    permission_classes = [permissions.IsAdminUser]


class TeamListView(generics.ListCreateAPIView):
    """Get, Post, Put, Delete API for Team"""

    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    authentication_classes = AUTHENTICATIONS
    permission_classes = PERMISSIONS

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)
