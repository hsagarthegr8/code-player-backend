from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, User

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    
       
