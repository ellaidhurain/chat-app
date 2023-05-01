from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(required=True)
    # username = serializers.CharField(required=True)
    # email = serializers.CharField(required=True)
    # password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password','first_name']
        extra_kwargs = {'password': {'write_only': True}}

        
    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #         first_name=validated_data['first_name']
    #     )
    #     return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_pic']
        extra_kwargs = {'user': {'write_only': True}}

    def create(self, validated_data): # validated_data - serialized request data
        user_data = validated_data.pop('user') 
        user = User.objects.create_user(**user_data) # when we creating user we should use create_user
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
    
        """
        pop is a built-in Python method that allows you to remove and 
        return an item from a dictionary by specifying its key.
        The line user_data = validated_data.pop('user') removes the item
        from validated_data that has the key 'user', 
        and assigns the corresponding value to the user_data variable.
    
        The **user_data syntax here is using the "unpacking" operator to 
        pass the contents of the user_data dictionary as keyword arguments 
        to the create() method. This is equivalent to calling User.objects.
        create(username=user_data['username'], email=user_data['email'], ...)
        with all the relevant fields from the user_data dictionary.
        
        1.pop(extract) the User object
        2.create User object
        3.create profile object that includes user as created User object 
        
        """
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title',)
        
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'

class OneChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneChat
        fields = '__all__'
        # depth = 1
        
        
class OneChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneChatMessage
        fields = '__all__'
        # depth = 1

class ChatRoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatRoom
        fields = '__all__'
        # depth = 1 # it will return all the details in the foreign key 
        # relationship instead of id 

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'
