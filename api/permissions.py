from rest_framework.permissions import BasePermission, SAFE_METHODS
from main import models


class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return obj.user == request.user or obj == request.user
        else:
            return True


class IsGroupOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
        

class IsGroupMember(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return models.Member.objects.filter(user=request.user, group=obj).exists()