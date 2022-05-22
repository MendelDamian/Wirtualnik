from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, ChangePasswordSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Updates and retrieves user accounts
    """

    queryset = User.available_objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)
    lookup_field = 'uuid'


class UserCreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Creates user accounts
    """

    queryset = User.available_objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)


class UpdatePasswordAPIView(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsUserOrReadOnly,)
    allowed_methods = ('PUT',)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get.
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
