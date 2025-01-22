from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DogPostViewSet, SignupView, LoginView, LogoutView, AdoptionView, CommentViewSet, CurrentUserView
router = DefaultRouter()
router.register(r'dogs', DogPostViewSet)
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = (
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('adoption/', AdoptionView.as_view(), name='adoption'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
)
