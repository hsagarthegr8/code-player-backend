from rest_framework.routers import DefaultRouter
from django.urls import path


from .accounts.views import UserViewSet
from .problems.views import ProblemViewSet

router = DefaultRouter()

router.register('accounts', UserViewSet, basename='accounts')
router.register('problems', ProblemViewSet, basename='problems')

urlpatterns = router.urls