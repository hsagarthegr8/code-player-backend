from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, User
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserViewSet(ModelViewSet):
    '''
    list: List All the Users
    create: Create a new user i.e. Register
    retrieve: Retrieve a single user instance based on username
    '''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self, *args, **kwargs):
        if self.action == 'create':
            return [AllowAny()]
        return super(UserViewSet, self).get_permissions(*args, **kwargs)

    def get_serializer_class(self):
        return super(UserViewSet, self).get_serializer_class()

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == 'me':
            return self.request.user

        return super(UserViewSet, self).get_object()
