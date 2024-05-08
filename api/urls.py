from django.urls import path
from . import views

urlpatterns = [
    path('group-create/', views.GroupChatCreateSerializer.as_view()),
    path('group-list/', views.GroupChatListSerializer.as_view()),
    path('admin-create/', views.AdminCreateSerializer.as_view()),
    path('request-create/', views.RequestCreateSerializer.as_view()),
    path('subscribers-list/', views.subscribers_list),
]