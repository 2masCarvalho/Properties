from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Review, Property, PropertyImage, Message



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ['user', 'address', 'phone_number', 'user_type', 'profile_picture', 'average_rating']



class ReviewSerializer(serializers.ModelSerializer):
    guest = ProfileSerializer(read_only=True)
    host = ProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'guest', 'host', 'rating', 'review_text', 'created_at']



class PropertySerializer(serializers.ModelSerializer):
    host = ProfileSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'host', 'title', 'description', 'location', 'price', 'area', 'num_bedrooms', 'num_bathrooms',
                  'elevator', 'parking_spaces', 'pool']



class PropertyImageSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image', 'uploaded_at']



class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']
