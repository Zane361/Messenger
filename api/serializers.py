from main import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.User
        # fields = ['username']
        exclude = ['id']

    
class UserImageSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.UserImages
        exclude = ['id']


class GroupSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Group
        # fields = ['code', 'name', 'description', 'user', 'date', 'banner', 'members_count', 'admins']
        exclude = ['id']

    def create(self, validated_data):
        banner = validated_data.pop('banner', None)
        group_instance = super(models.Group, self).create(validated_data)
        if banner:
            group_instance.banner = banner
            group_instance.save()
        
        return group_instance


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Member
        # fields = ['code', 'user', 'group', 'is_admin', 'join_date']
        exclude = ['id']


class AdminSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.GroupAdmin
        # fields = ['code', 'user', 'group', 'is_super']
        exclude = ['id']


class RequestSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Request
        # fields = ['code', 'user', 'group', 'date']
        exclude = ['id']

    
class MessageSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Message
        exclude = ['id']

    
class MessageFileSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.MessageFile
        exclude = ['id']