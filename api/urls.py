from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


from .accounts.views import UserViewSet
from .contest.views import ContestViewSet, ProblemViewSet, Playground

router = DefaultRouter()

router.register('accounts', UserViewSet, basename='accounts')
router.register(r'(?P<contest>[^/.]+)/problems',
                ProblemViewSet, basename='problems')
router.register('contests', ContestViewSet, basename='contests')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_jwt_token),
    path('playground/', Playground.as_view())
]
