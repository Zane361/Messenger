from . import serializers
from . import permissions
from main import models

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import * 


class UserViewSet(ViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [permissions.IsOwner]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                phone=request.data['phone'],
                )
            return Response(data=serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        user = self.request.user
        user_instance = models.User.objects.get(username=pk)
        print(user_instance)
        if user == user_instance:
            serializer = serializers.UserSerializer(user_instance, data=request.data, partial=True)
            if serializer.is_valid():
                if request.data['username']:
                    user.username = request.data['username']
                if request.data['password']:
                    user.set_password(request.data['password'])
                if request.data['phone']:
                    user.phone = request.data['phone']
                user.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk):
        user = request.user
        try:
            user_instance = models.User.objects.get(username=pk)
        except models.User.DoesNotExist:
            return Response(data={"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if user == user_instance:
            serializer = serializers.UserSerializer(user_instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, pk):
        try:
            user = models.User.objects.get(username=pk)
            user.delete()
            return Response(data={"detail": "Muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={'detail': "O'chirishda xatolik!"}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        code = request.query_params.get('code')
        try:
            group = models.Group.objects.get(code=code)
            members = models.Member.objects.filter(group=group)
            users = [member.user for member in members]
            serializer = serializers.UserSerializer(data=users, many=True)
            serializer.is_valid()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'Xatolik':"Xato kelib chiqdi!"})



class UserImageViewSet(ViewSet):

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'create' or self.action == 'destroy':
            permission_classes [permissions.IsOwner]
        return [permission() for permission in permission_classes]

    def create(self, request):
        ...

    def destroy(self, request):
        ...

    def list(self, request):
        ...


class GroupViewSet(ViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [permissions.IsOwner]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = serializers.GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = models.Group.objects.create(
                name = request.data['name'],
                description = request.data['description'],
                user = request.user,
                banner = request.data['banner'],
            )
            return Response(data=serializers.GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            group= models.Group.objects.get(code=pk)
        except models.Group.DoesNotExist:
            return Response(data={"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user == group.user:
            serializer = serializers.GroupSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        try:
            group = models.Group.objects.get(code=pk)
            is_member = models.Member.objects.filter(user=request.user, group=group)
        except models.Group.DoesNotExist:
            return Response(data={"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        if is_member.exists():
            serializer = serializers.GroupSerializer(group)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        try:
            group = models.Group.objects.get(code=pk)
        except models.Group.DoesNotExist:
            return Response(data={"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user == group.user:
            group.delete()
            return Response(data={"detail": "Group deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request):
        members = models.Member.objects.filter(user=request.user)
        groups = [member.group for member in members]
        serializer = serializers.GroupSerializer(groups, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MemberViewSet(ViewSet):
 
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [permissions.IsOwner]
        elif self.action == 'list':
            permission_classes = [permissions.IsGroupMember]
        return [permission() for permission in permission_classes]

    def destroy(self, request):
        ...

    def list(self, request):
        ...


class RequestViewSet(ViewSet):

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'list':
            permission_classes = [permissions.IsGroupOwner]
        return [permission() for permission in permission_classes]

    def create(self, request):
        ...

    def update(self, request):
        ...

    def list(self, request):
        ...


class MessageViewSet(ViewSet):

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [permissions.IsOwner]
        elif self.action == 'list':
            permission_classes = [permissions.IsGroupMember]
        return [permission() for permission in permission_classes]

    def create(self, request):
        ...

    def update(self, request):
        ...

    def destroy(self, request):
        ...

    def list(self, request):
        ...


class MessageFileViewSet(ViewSet):

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsOwner]
        elif self.action == 'list':
            permission_classes = [permissions.IsGroupMember]
        return [permission() for permission in permission_classes]

    def create(self, request):
        ...

    def destroy(self, request):
        ...

    def list(self, request):
        ...











































# class GroupChatListSerializer(generics.ListAPIView):
#     queryset = models.GroupChat.objects.all()
#     serializer_class = serializers.GroupChatSerializer


# class GroupChatCreateSerializer(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [BasicAuthentication]

#     def post(self, request):
#         try:
#             user = request.user
#             group = models.GroupChat.objects.create(
#                 name = request.POST['name'],
#                 description = request.POST['description'],
#                 user = user,
#                 banner = request.POST['banner'],
#             )
#             group_serializer = serializers.GroupChatSerializer(group)
#             admin = models.GroupAdmin.objects.create(
#                 user = user,
#                 group = group,
#                 is_super = True,
#             )
#             admin_serializer = serializers.AdminSerializer(admin)
#             subscriber = models.Subscriber.objects.create(
#                 user = user,
#                 group = group,
#                 is_admin = True,
#             )
#             subscriber_serializer = serializers.SubscriberSerializer(subscriber)
#             return Response({'group':group_serializer.data, 'admin':admin_serializer.data, 'subscriber':subscriber_serializer.data})
#         except:
#             return Response()


# class AdminCreateSerializer(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [BasicAuthentication]

#     def post(self, request):
#         try:
#             group = models.GroupChat.objects.get(code=request.POST['code'])
#             admin = models.GroupAdmin.objects.get(user=request.user, group=group)
#             if admin.is_super:
#                 created_admin = models.Admin.objects.create(
#                     user = models.User.objects.get(username = request.POST['user']),
#                     group = group,
#                     is_super = bool(request.POST['is_super'])
#                 )
#                 group_serializer = serializers.GroupChatSerializer(group)
#                 admin_serializer = serializers.AdminSerializer(created_admin)
#                 return Response({'group':group_serializer.data, 'admin':admin_serializer.data})
#             else:
#                 return Response({'Xatolik!':"Foydalanuvchida admin qo'shish huquqi yo'q!"})
#         except:
#             return Response()


# class RequestCreateSerializer(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [BasicAuthentication]

#     def post(self, request):
#         try:
#             user = request.user
#             group = models.GroupChat.objects.filter(name=request.POST['name'])[0]
#             models.Request.objects.create(
#                 user=user,
#                 group=group,
#             )
#             group_serializer = serializers.GroupChatSerializer(group)
#             return Response({'group':group_serializer.data})
#         except:
#             return Response()


# class RequestListSerializer(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [BasicAuthentication]
    
#     def get(self, request):
#         try:
#             user = request.user
#             permissions = models.GroupAdmin.objects.filter(user=user)
#             requests = []
#             for per in permissions:
#                 requests += list(models.Request.objects.filter(group=per.group))
#             request_serializers = serializers.RequestSerializer(requests, many=True)
#             return Response({'requests':request_serializers.data})
#         except:
#             return Response()
        

# class RequestAcceptSerializer(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [BasicAuthentication]

#     def put(self, request):
#         try:
#             user = request.user
#             requester = models.User.objects.get(username=request.data['user'])
#             group = models.GroupChat.objects.get(code=request.data['code'])
#             try:
#                 admin = models.GroupAdmin.objects.get(user=user, group=group)
#                 join_request = models.Request.objects.get(user=requester, group=group)
#             except:
#                 return Response({"Xatolik!":"Adminlik huquqi yo'q!"})
#             try:
#                 subscriber = models.Subscriber.objects.create(
#                     user = requester,
#                     group = group,
#                     is_admin = False,
#                 )
#                 join_request.is_active = False
#                 join_request.save()
#                 subscriber_serializer = serializers.SubscriberSerializer(subscriber)
#                 return Response({'subscriber':subscriber_serializer.data})
#             except:
#                 return Response()
#         except:
#             return Response()

# @api_view(['GET'])
# def subscribers_list(request):
#     try:
#         subscribers_serializer = serializers.SubscriberSerializer(models.Subscriber.objects.filter(group=models.GroupChat.objects.get(code=request.GET['code'])), many=True)
#         return Response({
#             'subscribers':subscribers_serializer.data
#         })
#     except:
#         return Response({'Xatolik!':"Guruh ko'di to'g'ri kiritilmadi!"})
    

