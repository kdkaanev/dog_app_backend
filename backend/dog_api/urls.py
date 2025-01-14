from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DogPostViewSet, SignupView, LoginView, sign_out, AdoptionView, CommentViewSet

router = DefaultRouter()
router.register(r'dogs', DogPostViewSet)
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = (
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', sign_out, name='logout'),
    path('adoption/', AdoptionView.as_view(), name='adoption'),
)
