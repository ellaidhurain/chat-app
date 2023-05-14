from django.urls import path,include,re_path
# from .views import TodoListView, check
from rest_framework import routers
from .views import *
from oauth2_provider.views import AuthorizationView, TokenView


# router = routers.DefaultRouter()
# router.register(r'chat_rooms', GroupChatRoomViewSet) # chatRoom CRUD

from django.views.generic import TemplateView
from social_django.urls import urlpatterns as social_django_urlpatterns


urlpatterns = [
      
    # path('oauth2callback/', TemplateView.as_view(template_name='oauth2_callback.html')),
    # path('oauth2/authorize/', AuthorizationView.as_view(), name='authorize'),
    # path('oauth2/token/', TokenView.as_view(), name='token'),
    
    # path('todo/', TodoListView.as_view()), 
    # path('check/', check), 
    
    # user CRUD
    path('create_user', create_user, name='create_user'),
    path('user_signup',register_user, name='create_user'),
    path('user_list', get_user, name='get_user'),
    path('user_profile/get/<int:user_id>', get_user_profile, name='get_user'),
    path('user/<int:user_id>', update_user, name='update_user'),
    path('user/<int:user_id>', delete_user, name='delete_user'),
    path('login', login_user, name='login'),
    
    # create a friend request
    path('friend-requests/send', send_friend_request, name='send_friend_request'),
    path('friend-requests/accept/<int:friend_request_id>', respond_to_friend_request, name='accept_friend_request'),
    path('friend-requests-list', friend_request_list, name='friend_request_list'),  
    path('list_friends', list_friends, name='list_friends'),
    
    # group chat room
    # path('', include(router.urls)),
    path('group_chat_room/create', GroupChatRoomViewSet.as_view({'post': 'create'}), name='create_chatroom'),
    path('group_chat_room/update/<int:chat_room_id>', GroupChatRoomViewSet.as_view({'put': 'update'}), name='update_chatroom'),
    path('group_chat_room/get', GroupChatRoomViewSet.as_view({'get': 'list'}), name='get_chatroom'),
    path('group_chat_room/delete', GroupChatRoomViewSet.as_view({'destroy': 'delete'}), name='delete_chatroom'),
    
    # group chat messages for particular room
    path('group_message/get/<int:chat_room_id>', GroupMessageViewSet.as_view({'get': 'list'}), name='get_group_message'),
    path('group_message/create', GroupMessageViewSet.as_view({'post': 'create'}), name='send_group_message'),
    path('group_message/update', GroupMessageViewSet.as_view({'put': 'update'}), name='update_group_message'),
    path('group_message/delete', GroupMessageViewSet.as_view({'delete': 'destroy'}), name='delete_group_message'),
    
    # one chat room
    path('one_chat_room/create', OneChatViewSet.as_view({'post': 'create'}), name='create_chat_room'),
    path('one_chat_room/get', OneChatViewSet.as_view({'get': 'list'}), name='get_one_chat_room'),
    path('one_chat_room/update', OneChatViewSet.as_view({'put': 'update'}), name='update_one_chat_room'),
    path('one_chat_room/delete', OneChatViewSet.as_view({'destroy': 'delete'}), name='delete_one_chat_room'),
    
    # one chat room messages
    path('one_chat_message/send', OneChatMessageViewSet.as_view({'post': 'create'}), name='one_chat_room_list'),
    path('one_chat_message/get/<int:chat_room_id>', OneChatMessageViewSet.as_view({'get': 'list'}), name='get_one_chat_message'),
    path('one_chat_message/update', OneChatMessageViewSet.as_view({'put': 'update'}), name='update_one_chat_message'),
    path('one_chat_message/delete/<int:chat_room_id>/<int:message_id>', OneChatMessageViewSet.as_view({'delete': 'destroy'}), name='delete_one_chat_message'),
    
   
    # regex method of url
    # re_path(r'^message/(?P<chat_room_id>\d+)/create/$', GroupMessageViewSet.as_view({'post': 'create'}), name='create_message'),
    # re_path(r'^message/(?P<chat_room_id>\d+)/list/$', GroupMessageViewSet.as_view({'get': 'list'}), name='list_message'),
    
    
    # path('<str:room_name>', room, name='room')
]
urlpatterns += social_django_urlpatterns