from main import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username']


class GroupChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = models.GroupChat
        fields = ['code', 'name', 'description', 'owner', 'date', 'banner', 'subscribers_count', 'admins']


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscriber
        fields = ['code', 'user', 'group', 'is_admin', 'join_date']


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupChatSerializer(read_only=True)
    class Meta:
        model = models.Admin
        fields = ['code', 'user', 'group', 'is_super']


class RequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupChatSerializer(read_only=True)
    class Meta:
        model = models.Request
        fields = ['code', 'user', 'group', 'date']