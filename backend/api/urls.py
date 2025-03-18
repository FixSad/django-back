from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TestViewSet, ResultsViewSet, UserProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='me'),
    path('add-test/', TestViewSet.as_view({'post': 'add_test'}), name='add_test'),
    path('add-result/', ResultsViewSet.as_view({'post': 'add_result'}), name='add_result'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]