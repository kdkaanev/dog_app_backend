from rest_framework import serializers
from .models import DogPost, DogUser, Message, Comment


class DogPostSerializer(serializers.ModelSerializer):
    dog_user_id = serializers.SerializerMethodField()
    dog_user_name = serializers.SerializerMethodField()

    class Meta:
        model = DogPost
        fields = ['id', 'title', 'breed', 'photo_url', 'description', 'last_seen_location', 'date_posted', 'status',
                  'user', 'dog_user_id', 'dog_user_name', 'has_messages']
        read_only_fields = ('id', 'date_posted', 'user',)

    @staticmethod
    def get_dog_user_id(obj):
        dog_user = DogUser.objects.filter(user=obj.user).first()
        return dog_user.id if dog_user else None

    @staticmethod
    def get_dog_user_name(obj):
        dog_user = DogUser.objects.filter(user=obj.user).first()
        return dog_user.first_name if dog_user else None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'dog_post', 'content', 'created_at']
        read_only_fields = ['user', 'dog_post', 'created_at']  # Prevent these fields from being editable


class DogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'location', 'user', 'full_name', 'received_messages']


class LightDogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogUser
        fields = ['id', 'first_name', 'full_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = LightDogUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'message', 'sender', 'recipient', 'dog', 'created_at']
        read_only_fields = ['sender', 'recipient', 'dog', 'created_at']
