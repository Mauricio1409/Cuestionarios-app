from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer as DjoserUserCreatePasswordRetypeSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(DjoserUserCreatePasswordRetypeSerializer):
    name = serializers.CharField(required=True, max_length=100)

    class Meta(DjoserUserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "email", "password", "name")


class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "is_active", "created_at")