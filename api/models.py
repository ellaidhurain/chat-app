from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from oauth2_provider.models import AbstractApplication
from django.conf import settings

class Application(AbstractApplication):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allowed_scopes = models.CharField(
        max_length=100,
        blank=True,
        help_text='Space separated list of allowed scopes for the application.'
    )

    class Meta(AbstractApplication.Meta):
        swappable = 'OAUTH2_PROVIDER_APPLICATION_MODEL'


class Todo(models.Model):
    title = models.CharField(max_length=70)
    
    def __str__(self):
        return Todo.title
    

  # DATA BASE design
  # OneChat is entity which means a real world object in the
  # -form of physical or conceptual.
  # Physical means we can touch it like person, car, dog.
  # Conceptual means the imaginary object like messages , chatroom.
  # Attributes means the properties of the objects like name, age ,email.
  # Before creating table we need to find out the entities and their attributes from requirements
  # Then we need to find out the relationship between two tables or entities.
  # we need to save commonly shared attributes separately then get the attribute
  # -using foreign key relationship or many to many relationship based on requirements. 
  # we can also use abstract models.
    
# The purpose of abstract models is to provide a way to define common fields 
# -or behavior that can be reused across multiple models in an application. 
# abstract model is not saved to database

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()        

# user profile 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )

    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friends_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends_as_user2', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


# one to one chat room chat room is stored in this table
class OneChat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=True) # chat room name
    user1 = models.ForeignKey(User, related_name='chat_rooms_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chat_rooms_as_user2', default=None, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=models.Q(user2__isnull=True) | models.Q(user2__in=models.Subquery(
    #                 Friendship.objects.filter(user1=models.OuterRef('user1')).values('user2')
    #             )),
    #             name='user2_is_friend_of_user1'
    #         )
    #     ]


   # messages for one to one chat room is saved in this table
   # sender and receiver is imported from User table
   # chat room id is received from OneChat table
   
   
class OneChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    chat_room_id = models.ForeignKey(OneChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', default=None, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='files',validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg'])], null=True)
    
    
 # many to many chat room (group chat) is saved in this table.
 # members field is have many to many relationship with User table.
 # one user will able to send message to many user.
 # one user will get message from many user.
 
class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=True) # chat room name
    members = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_chat_rooms", null=True, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        super().clean()
        if self.members.count() < 2:
            raise ValidationError('A chat room must have at least two members.')
    
   # messages for many to many chat room is saved in this table
   # sender is imported from User table
   # chat room id is received from ChatRoom table

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(max_length=500) # message field
    timestamp = models.DateTimeField(auto_now_add=True) # get the object created time
    sender = models.ForeignKey(User, on_delete=models.CASCADE) # get the sender id as foreign key
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE) # get the chatroom id as foreign key
    attachment = models.FileField(upload_to='files',validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg'])], null=True)
    
    def clean(self):
        super().clean()
        if self.sender not in self.chat_room_id.members.all():
            raise ValidationError('The sender must be a member of the chat room.')

    # receiver is added in this table
    # get a message from Message model and receiver from User model 
    
class Recipient(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    
    