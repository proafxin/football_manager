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


# class UserDetailView(generics.RetrieveAPIView):
#     """
#     User information.
#     """

#     queryset = UserModel.objects.all()
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserDetailSerializer
