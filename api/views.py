from datetime import timedelta, timezone
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .models import Todo
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from .decorators import *
from django.db.models import Q
import logging
from oauth2_provider.decorators import protected_resource
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import login
from django.views.generic import TemplateView
# from social_django.utils import psa
from django.http import Http404, JsonResponse
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.models import get_application_model
from oauth2_provider.views import AuthorizationView as BaseAuthorizationView
from oauth2_provider.views import TokenView as BaseTokenView
import requests
# from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.middleware import csrf
from django.middleware.csrf import get_token
import jwt
from rest_framework_simplejwt.tokens import RefreshToken



# class MyApiView(ProtectedResourceView):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse({"message": "Hello, OAuth2 user!"})


# class GoogleLoginView(View):
#     @psa("social:begin", "google-oauth2")
#     def get(self, request, *args, **kwargs):
#         return self.backend(request, *args, **kwargs)

#     def backend(self, request, *args, **kwargs):
#         return redirect(reverse("oauth2_callback"))


# class GoogleCallbackView(TemplateView):
#     template_name = "oauth2_callback.html"

#     @psa("social:complete", "google-oauth2")
#     def get(self, request, *args, **kwargs):
#         user = request.backend.do_auth(request.GET.get("access_token"))
#         if user:
#             login(request, user)
#             return redirect(reverse("home"))
#         else:
#             return self.render_to_response({})


# class AuthorizationView(BaseAuthorizationView):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             application = Application.objects.get(
#                 client_id=self.request.GET.get("client_id", "")
#             )
#             if application.owner == request.user:
#                 return super().get(request, *args, **kwargs)
#         return redirect(reverse("login"))


# class TokenView(BaseTokenView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 200:
#             data = response.json()
#             data["user_id"] = request.user.id
#             response = JsonResponse(data)
#         return response


class TodoListView(generics.ListAPIView):
    model = Todo
    serializer_class = TodoSerializer


# def check(request, *args, **kwargs):
#     context = {"firstname": "ellaidhurai", "lastname": "ed"}
#     return render(request, "frontend/index.html", context)


# @api_view(["POST"])
# def room(request, room_name):
#     pass


@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Check if username is already taken
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if email is already registered
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save user object
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @func_token_required
@api_view(["GET"])
def get_user(request):
    try:
        user = User.objects.all()
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@func_token_required
def get_user_profile(request, user_id):
    try:
        user = Profile.objects.get(user=user_id)

    except Profile.DoesNotExist:
        return Response({"error": "no user found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@func_token_required
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@func_token_required
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def register_user(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        # Check if username is already taken
        if User.objects.filter(username=request.data["user"]["username"]).exists():
            return Response(
                {"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if email is already registered
        if User.objects.filter(email=request.data["user"]["email"]).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save user object
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    # get user input
    username = request.data["username"]
    password = request.data["password"]
    
     # check if user exists and is active
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    elif not user.is_active:
        return Response({"detail": "User is inactive"}, status=status.HTTP_400_BAD_REQUEST)

   # send payload to verify in decode
    payload = {
        "user": {
            "id": user.id,
            "email": user.email,
            "exp": (datetime.utcnow() + timedelta(minutes=15)).isoformat(),
            "iat": datetime.utcnow().isoformat(),
        }
    }
     # generate JWT tokens
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = RefreshToken.for_user(user)

    # token = {"refresh": str(refresh_token), "access": access_token}

    # create response object
    response = Response(status=status.HTTP_200_OK)
    response['Authorization'] = f'Bearer {access_token}'
    response['Refresh-Token'] = str(refresh_token)
    return response


# @api_view(["POST"])
# def login_user(request):
#     # get user input
#     username = request.data["username"]
#     password = request.data["password"]

#     # check email has registered
#     user = authenticate(request, username=username, password=password)

#     token_url = "http://localhost:8000/o/token/"
#     data = {
#         "grant_type": "password",
#         "username": user.username,
#         "password": password,
#         "client_id": settings.CLIENT_ID,
#         "client_secret": settings.CLIENT_SECRET,
#     }

#     try:
#         response = requests.post(token_url, data=data)
#         response.raise_for_status()
#         full_token = response.json()
#         access_token = response.json().get("access_token")
#         csrf_token = csrf.get_token(request)

#         headers = {
#             "Authorization": f"Bearer {access_token}",
#              'X-CSRFToken': csrf_token,
#              'Content-Type': 'application/json'   
#                 }
#         res = Response()
#         # res.set_cookie(
#         #     key=settings.TOKEN_COOKIE_NAME,
#         #     value=access_token,
#         #     max_age=settings.TOKEN_EXPIRATION_TIME,
#         #     secure=settings.SESSION_COOKIE_SECURE,
#         #     httponly=True,
#         #     samesite=settings.SESSION_COOKIE_SAMESITE,
#         # )
#         # print("Cookie:", res.cookies)
#         # print('Headers:', res.headers)
#     except requests.exceptions.HTTPError as error:
#         return Response(
#             {"detail": "Could not get access token"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )

#     # return token in response
#     return Response({"oauth_token": full_token}, status=status.HTTP_200_OK, headers=headers)


# @api_view(["POST"])
# def token(request):
#     r = requests.post(
#         "http://localhost:8000/o/token/",
#         data={
#             "grant_type": "password",
#             "username": request.data["username"],
#             "password": request.data["password"],
#             "client_id": settings.CLIENT_ID,
#             "client_secret": settings.CLIENT_SECRET,
#         },
#     )
#     return Response(r.json())


# @api_view(["POST"])
# def refresh_token(request):
#     r = requests.post(
#         "http://localhost:8000/o/token/",
#         data={
#             "grant_type": "refresh_token",
#             "refresh_token": request.data["refresh_token"],
#             "client_id": settings.CLIENT_ID,
#             "client_secret": settings.CLIENT_SECRET,
#         },
#     )
#     return Response(r.json())


@csrf_protect
@func_token_required
@api_view(['POST'])
def send_friend_request(request):
    from_user = request.user
    to_user_id = request.data.get('to_user')
    if not to_user_id:
        return Response({'error': 'Please provide a to_user_id.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        to_user = User.objects.get(pk=to_user_id)
    except User.DoesNotExist:
        return Response({'error': 'Invalid to_user_id.'}, status=status.HTTP_400_BAD_REQUEST)
    if from_user == to_user:
        return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    if Friendship.objects.filter(Q(user1=from_user, user2=to_user) | Q(user1=to_user, user2=from_user)).exists():
        return Response({'error': 'You are already friends with this user.'}, status=status.HTTP_400_BAD_REQUEST)
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({'error': 'You have already sent a friend request to this user.'}, status=status.HTTP_400_BAD_REQUEST)

    csrf_token = csrf.get_token(request)
    headers = {'X-CSRFToken': csrf_token}

    
    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    serializer = FriendRequestSerializer(friend_request)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# get pending friend request list 
@func_token_required
@api_view(['GET'])
def friend_request_list(request):
    # Get all pending friend requests for the current authenticated user
    friend_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    # Serialize the friend requests
    serialized_friend_requests = FriendRequestSerializer(friend_requests, many=True)
    # Return the serialized friend requests in the response
    return Response(serialized_friend_requests.data, status=status.HTTP_200_OK)

@func_token_required
@api_view(['POST'])
def respond_to_friend_request(request, friend_request_id):
    status_value = request.data.get('status', '').lower()
    if not friend_request_id or not status_value:
        return Response({'error': 'Please provide a friend_request_id and a status.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        friend_request = FriendRequest.objects.get(from_user_id=friend_request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Invalid friend_request_id.'}, status=status.HTTP_400_BAD_REQUEST)
    if friend_request.to_user != request.user:
        return Response({'error': 'You are not authorized to respond to this friend request.'}, status=status.HTTP_401_UNAUTHORIZED)
    if status_value == 'accepted':
        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.status = status_value
        friend_request.save()
        return Response({'success': 'Friend request accepted.'}, status=status.HTTP_200_OK)
    if status_value == 'rejected':
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'success': 'Friend request rejected.'}, status=status.HTTP_200_OK)
    serializer = FriendRequestSerializer(friend_request)
    csrf_token = get_token(request)
    headers = {'X-CSRFToken': csrf_token}
    return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

# accepted friends list
@func_token_required
@api_view(['GET'])
def list_friends(request):
    user = request.user
    # get all the friendships that involve the request user
    friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
    friend_ids = []
    for friendship in friendships:
        # get all the id of friends other than request user,
        # then append that ids in list
        if friendship.user1 == user:
            friend_ids.append(friendship.user2.id)
        else:
            friend_ids.append(friendship.user1.id)
            
        # find that list of ids in User model and filter the users store in friends variable
    friends = User.objects.filter(id__in=friend_ids)
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class OneChatViewSet(GenericViewSet):
    queryset = OneChat.objects.all()
    serializer_class = OneChatSerializer
    # Serializers typically provide methods for both serialization
    # (converting data to a specific format) and deserialization
    # (converting data from a specific format back to its original form).

    @token_required
    def create(self, request):
        user1 = request.user
        user2_id = request.data.get("user2")

        if not user2_id:
            return Response(
                {"error": "user2_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response(
                {"error": f"user with id {user2_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if user1 and user2 have a friendship relationship
        friendship1 = Friendship.objects.filter(user1=user1, user2=user2).first()
        friendship2 = Friendship.objects.filter(user1=user2, user2=user1).first()
        
        if not friendship1 and not friendship2:
            return Response(
                {"error": f"No friendship relationship between users {user1.id} and {user2.id} found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user1 == user2:
            return Response(
                {"error": "user1 and user2 cannot be the same"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_chatroom = OneChat.objects.filter(
            name=request.data.get("name"),
        ).first()

        if existing_chatroom:
            raise ValidationError("A chat room with the same name already exists.")

        # check if chat room already exists between user1 and user2
        chat = OneChat.objects.filter(user1=user1.id, user2=user2.id).first()

        if chat is not None:
            return Response(
                {
                    "error": f"chat room between users {user1.id} and {user2.id} already exists"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create new chat room
        chat = OneChat(user1=user1, user2=user2)

        serializer = OneChatSerializer(
            chat,
            data={
                  "name": request.data.get("name"),
                  "user1": request.user.id,
                  "user2": user2.id,
                  },
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @token_required
    def list(self, request):
        try:
            chat_room = OneChat.objects.all()
        except OneChat.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)

        serializer = OneChatSerializer(chat_room, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @token_required
    def update(self, request):
        chat_room_id = request.data.get("chat_room_id")
        instance = get_object_or_404(OneChat, id=chat_room_id)

        if request.user != instance.user1:
            return Response(
                {"error": "You are not a member of this chat room"},
                status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "user1": request.user.id,
            "user2": request.data.get("user2"),
            "name": request.data.get("name"),
        }

        if data["user1"] == data["user2"]:
            return Response(
                {"error": "user1 and user2 should not have same id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def destroy(self, chat_room_id):
        instance = get_object_or_404(OneChat, id=chat_room_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OneChatMessageViewSet(GenericViewSet):
    # select_related is useful to make fast queries
    # prefetch_related() is used to fetch related objects in a separate query, and then cache them for later use. It's used for many-to-many and reverse foreign key relationships, where each object has many related objects.
    queryset = OneChatMessage.objects.select_related("sender")
    serializer_class = OneChatMessageSerializer

    @token_required
    def create(self, request):
        chat_room_id = request.data.get("chat_room_id", None)
        try:
            chat_room_id = OneChat.objects.get(id=chat_room_id)
        except OneChat.DoesNotExist:
            return Response(
                {"error": f"Chat room with id={chat_room_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        receiver_id = request.data.get("receiver", None)
        # Get the receiver from the receiver_id parameter
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response(
                {"error": f"User with id={receiver_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create a new message object and populate it with data from the request
        message = OneChatMessage(
            chat_room_id=chat_room_id, sender=request.user, receiver=receiver
        )

        if "attachment" in request.data:
            # save the attachment to a FileField
            message.attachment.save(
                request.data["attachment"].name, request.data["attachment"], save=True
            )
        # save the message object
        message.save()
        # serializer = OneChatMessageSerializer(message)
        serializer = OneChatMessageSerializer(
            message,
            data={
                "chat_room_id": chat_room_id.id,
                "sender": request.user.id,
                "receiver": receiver.id,
                "text": request.data.get("text"),
            },
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def list(self, request, chat_room_id):
        chat_room = get_object_or_404(OneChat, id=chat_room_id)
        if request.user.id != chat_room.user1.id and chat_room.user2.id:
            return Response(
                {"error": "You are not a member of this chat room."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = OneChatMessage.objects.filter(chat_room_id=chat_room_id)
        serializer = OneChatMessageSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @token_required
    def update(self, request):
        chat_room_id = request.data.get("chat_room_id")
        message_id = request.data.get("id")

        instance = get_object_or_404(
            OneChatMessage, id=message_id, chat_room_id=chat_room_id
        )

        if request.user != instance.sender:
            return Response(
                {"error": "You are not the sender of this message."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            serializer = self.get_serializer(
                instance,
                data={
                    "chat_room_id": chat_room_id,
                    "sender": request.user.id,
                    "text": request.data.get("text"),
                },
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except OneChatMessage.DoesNotExist:
            return Response(
                {"error": "Not a valid chat_room_id or sender_id "},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @token_required
    def destroy(self, request, chat_room_id, message_id):
        message = get_object_or_404(
            OneChatMessage, id=message_id, chat_room_id=chat_room_id
        )
        if request.user != message.sender:
            return Response(
                {"error": "You are not the sender of this message."},
                status=status.HTTP_403_FORBIDDEN,
            )
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupChatRoomViewSet(GenericViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    @token_required
    def create(self, request):
        try:
            # Check if a ChatRoom with the same name already exists
            existing_chatroom = ChatRoom.objects.filter(
                name=request.data.get("name"),
            ).first()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if existing_chatroom is not None:
            raise ValidationError("A chat room with the same name already exists.")

        created_by = request.user

        try:
            user = User.objects.get(id=created_by.id)
        except User.DoesNotExist:
            return Response(
                {"error": "User matching query does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        members = request.data.get("members")

        # Check if the request user is already a member of this room
        if request.user.id in members:
            return Response(
                {"error": "Request user is already a member of this room."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invalid_ids = []
        for member_id in members:
            try:
                User.objects.get(id=member_id)
            except User.DoesNotExist:
                invalid_ids.append(member_id)

        if invalid_ids:
            raise serializers.ValidationError(
                f"The following user IDs are not valid user: {', '.join(str(uid) for uid in invalid_ids)}"
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @token_required
    def list(self, request):
        try:
            queryset = self.get_queryset()  # This will return ChatRoom.objects.all()
            serializer = self.get_serializer(queryset, many=True)

            # This will return ChatRoomSerializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not found"}, status=status.HTTP_404_BAD_REQUEST)

    @token_required
    def update(self, request, chat_room_id):
        instance = get_object_or_404(ChatRoom, id=chat_room_id)
        members = request.data.get("members")

        try:
            # Check if a ChatRoom with the same name already exists
            existing_chatroom = ChatRoom.objects.filter(
                name=request.data.get("name"),
            ).first()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if existing_chatroom is not None:
            raise ValidationError("A chat room with the same name already exists.")

        created_by = request.user

        try:
            user = User.objects.get(id=created_by.id)
        except User.DoesNotExist:
            return Response(
                {"error": "User matching query does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        members = request.data.get("members")

        # Check if the request user is already a member of this room
        if request.user.id in members:
            return Response(
                {"error": "Request user is already a member of this room."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invalid_ids = []
        for member_id in members:
            try:
                User.objects.get(id=member_id)
            except User.DoesNotExist:
                invalid_ids.append(member_id)

        if invalid_ids:
            raise serializers.ValidationError(
                f"The following user IDs are not valid user: {', '.join(str(uid) for uid in invalid_ids)}"
            )

        try:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def destroy(self, request):
        chat_room_id = request.data.get("chat_room_id")
        instance = get_object_or_404(ChatRoom, id=chat_room_id)
        if request.user not in instance.members:
            return Response(
                {"error": "You are not the creator of this chatroom."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupMessageViewSet(GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @token_required
    def create(self, request):
        chat_room_id = request.data.get("chat_room_id")
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        # check if the current user is a member of the chat room
        if request.user not in chat_room.members.all():
            return Response(
                {"error": "You are not a member of this chat room."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create the message object
        message = Message(sender=request.user, chat_room_id=chat_room)
        # get the message text from the request data
        message.text = request.data.get("text", "")

        if "attachment" in request.data:
            # save the attachment to a FileField
            message.attachment.save(
                request.data["attachment"].name, request.data["attachment"], save=True
            )
        # save the message object
        message.save()

        # create recipient objects for all members of the chat room except the sender
        # send message to receiver
        recipients = []
        for member in chat_room.members.exclude(id=request.user.id):
            recipient = Recipient(message=message, recipient=member)
            recipients.append(recipient)
        # save the recipient objects
        Recipient.objects.bulk_create(recipients)
        # serialize the message object
        serializer = self.get_serializer(message)
        # return the serialized message object as a JSON response
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @token_required
    def list(self, request, chat_room_id):
        # get the chat room object
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        # check if the current user is a member of the chat room
        if request.user not in chat_room.members.all():
            return Response(
                {"error": "You are not a member of this chat room."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # get all the messages for the chat room
        messages = Message.objects.filter(chat_room_id=chat_room).order_by("timestamp")
        # mark all messages as read
        for message in messages:
            recipient = Recipient.objects.filter(
                message=message, recipient=request.user, is_read=False
            )
            recipient.update(is_read=True)

        # serialize the messages to JSON
        serializer = MessageSerializer(messages, many=True)
        # return the serialized messages as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    @token_required
    def update(self, request, chat_room_id):
        instance = get_object_or_404(Message, id=chat_room_id)

        try:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def destroy(self, chat_room_id):
        instance = get_object_or_404(Message, id=chat_room_id)
        instance.delete

        return Response(status.HTTP_204_NO_CONTENT, {"message": "successfully deleted"})
