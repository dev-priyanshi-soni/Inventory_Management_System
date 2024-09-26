from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Item Serializer
class ItemSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at']
