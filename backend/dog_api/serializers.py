from rest_framework import serializers
from .models import DogPost, DogUser


class DogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPost
        fields = '__all__'

from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'dog_post', 'content', 'created_at']
        read_only_fields = ['user', 'dog_post', 'created_at']  # Prevent these fields from being editable
class DogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogUser
        fields = ['id', 'phone_number', 'full_name',]
