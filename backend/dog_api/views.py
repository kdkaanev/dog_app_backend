import token

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from .models import Comment, Message
from .serializers import DogPostSerializer, CommentSerializer, MessageSerializer

from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from .models import DogPost, DogUser
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from .serializers import DogUserSerializer
from rest_framework.authtoken.models import Token


class DogPostViewSet(ModelViewSet):
    queryset = DogPost.objects.all().order_by('-date_posted')
    serializer_class = DogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_field = ['type', 'breed', 'last_seen_location']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Viewing posts
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:  # Creating, editing, or deleting posts
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        posts = DogPost.objects.filter(user=user)  # Filter posts by the logged-in user
        serializer = DogPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(username=username, password=password)

        # Check if authentication failed
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Log in user
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        csrf_token = get_token(request)

        # Get related DogUser instance (if exists)
        dog_user = getattr(user, 'dog_user', None)

        # Prepare DogUser data
        dog_user_data = DogUserSerializer(dog_user).data if dog_user else None
        if dog_user:
            dog_user_data = {
                "id": dog_user.id,
                "phone": dog_user.phone_number if hasattr(dog_user, "phone_number") else None,

            }

        # Return response
        response = Response({
            "id": user.id,
            "username": username,
            "dog_user": dog_user_data,
            "message": "Login successful"
        }, status=status.HTTP_200_OK)

        # Set CSRF token as a cookie
        response.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,  # Allow frontend to access it
            secure=False,  # TODO Set to False in local dev (use True for HTTPS)

            samesite="Lax"
        )

        return response


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        dog_user = getattr(user, 'dog_user', None)
        dog_user_data = DogUserSerializer(dog_user).data if dog_user else None

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "dog_user": dog_user_data,
        })

    def patch(self, request):
        # Extract and validate data
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        location = request.data.get('location')

        if not any([first_name, last_name, phone_number, location]):
            return Response(
                {"error": "No fields provided to update."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update user profile
        try:
            user_profile = request.user.dog_user  # Assuming DogUser is related to the user
            if first_name:
                user_profile.first_name = first_name
            if last_name:
                user_profile.last_name = last_name
            if phone_number:
                user_profile.phone_number = phone_number
            if location:
                user_profile.location = location
            user_profile.save()

            return Response(
                {
                    "username": request.user.username,
                    "message": "Profile updated successfully!"
                },
                status=status.HTTP_200_OK,
            )
        except AttributeError:
            return Response(
                {"error": "User profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.perform_logout(request)

    def delete(self, request):
        return self.perform_logout(request)

    @staticmethod
    def perform_logout(request):
        logout(request)
        response = Response({"message": "Logged out successfully."}, status=200)
        response.delete_cookie("sessionid", path="/", domain=None)
        response.delete_cookie("csrftoken", path="/", domain=None)
        return response


class AdoptionView(APIView):
    permission_classes = [AllowAny]  # Only authenticated users can adopt

    @staticmethod
    def post(request):
        dog_post_id = request.data.get("dog_post_id")  # ID of the dog post the user wants to adopt

        if not dog_post_id:
            return Response({"error": "Dog post ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            dog_post = DogPost.objects.get(id=dog_post_id)
        except DogPost.DoesNotExist:
            return Response({"error": "Dog post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the dog is already adopted
        if dog_post.status == "adopted":
            return Response({"error": "This dog has already been adopted"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the dog is found (and eligible for adoption)
        if dog_post.status != "found":
            return Response({"error": "You can only adopt found dogs"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the dog as adopted
        dog_post.status = "adopted"
        dog_post.save()

        return Response({"message": "Dog adopted successfully"}, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user and the related dog post
        dog_post = DogPost.objects.get(id=self.request.data['dog_post'])
        serializer.save(user=self.request.user, dog_post=dog_post)

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        recipient_id = self.request.data['recipient']
        dog_id = self.request.data['dog']

        try:
            recipient = DogUser.objects.get(id=recipient_id)
            dog = DogPost.objects.get(id=dog_id)
        except DogPost.DoesNotExist:
            raise serializers.ValidationError("Dog post not found")
        except DogUser.DoesNotExist:
            raise serializers.ValidationError("User not found")
        serializer.save(sender=self.request.user, recipient=recipient, dog=dog)
