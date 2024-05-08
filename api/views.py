from . import serializers
from main import models
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics


class GroupChatListSerializer(generics.ListAPIView):
    queryset = models.GroupChat.objects.all()
    serializer_class = serializers.GroupChatSerializer


class GroupChatCreateSerializer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            group = models.GroupChat.objects.create(
                name = request.POST['name'],
                description = request.POST['description'],
                owner = user,
                banner = request.POST['banner'],
            )
            group_serializer = serializers.GroupChatSerializer(group)

            admin = models.Admin.objects.create(
                user = user,
                group = group,
                is_super = True,
            )
            admin_serializer = serializers.AdminSerializer(admin)
            return Response(group_serializer.data, admin_serializer.data)
        except:
            return Response(None)


class AdminCreateSerializer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            group = models.GroupChat.objects.get(code=request.POST['code'])
            admin = models.Admin.objects.get(user=request.user, group=group)
            if admin.is_super:
                created_admin = models.Admin.objects.create(
                    user = models.User.objects.get(username = request.POST['user']),
                    group = group,
                    is_super = bool(request.POST['is_super'])
                )
                group_serializer = serializers.GroupChatSerializer(group)
                admin_serializer = serializers.AdminSerializer(created_admin)
                return Response(group_serializer.data, admin_serializer)
            else:
                return Response({'Xatolik!':"Foydalanuvchida admin qo'shish huquqi yo'q!"})
        except:
            return Response()


class RequestCreateSerializer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            group = models.GroupChat.objects.get(name=request.POST['name'])
            req = models.Request.objects.create(
                user=user,
                group=group,
            )
            user_serializer = serializers.UserSerializer(user)
            group_serializer = serializers.GroupChatSerializer(group)
            request_serializer = serializers.RequestSerializer(req)
            return Response({'user':user_serializer.data, 'group':group_serializer.data, 'request':request_serializer.data})
        except:
            return Response()


@api_view(['GET'])
def subscribers_list(request):
    try:
        subscribers_serializer = serializers.SubscriberSerializer(models.Subscriber.objects.filter(group=models.GroupChat.objects.get(code=request.GET['code'])), many=True)
        return Response({
            'subscribers':subscribers_serializer.data
        })
    except:
        return Response({'Xatolik!':"Guruh ko'di to'g'ri kiritilmadi!"})
