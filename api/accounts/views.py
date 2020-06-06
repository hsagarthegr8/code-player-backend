from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, User
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self, *args, **kwargs):
        if self.action == 'create':
            return [AllowAny()]
        return super(UserViewSet, self).get_permissions(*args, **kwargs)
