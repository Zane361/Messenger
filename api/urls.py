from django.urls import path, include
from rest_framework import routers
from main import models
from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename=models.User)
router.register(r'group', views.GroupViewSet, basename=models.Group)

urlpatterns = [
    path('', include(router.urls)),
]
    # path('group-create/', views.GroupChatCreateSerializer.as_view()),
    # path('group-list/', views.GroupChatListSerializer.as_view()),
    # path('admin-create/', views.AdminCreateSerializer.as_view()),
    # path('request-create/', views.RequestCreateSerializer.as_view()),
    # path('request-list/', views.RequestAcceptSerializer.as_view()),
    # path('request-accept/', views.RequestAcceptSerializer.as_view()),
    # path('subscribers-list/', views.subscribers_list),