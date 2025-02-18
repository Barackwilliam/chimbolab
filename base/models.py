from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, help_text="Enter your name", verbose_name="Name")
    email = models.EmailField(unique=True, null=True, help_text="Enter your email", verbose_name="Email")
    bio = models.TextField(null=True, help_text="A brief description about yourself", verbose_name="Biography")
    #avatar = models.ImageField(null=True, default="avatar.svg", help_text="Upload an avatar", verbose_name="Avatar")
    avatar = CloudinaryField('avatar')
    # , null=True, default="avatar.svg", help_text="Upload an avatar"
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Topic(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the topic name", verbose_name="Topic")

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Select the host of the room", verbose_name="Host")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, help_text="Select a topic for the room", verbose_name="Topic")
    name = models.CharField(max_length=200, help_text="Enter the room name", verbose_name="Room Name")
    description = models.TextField(null=True, blank=True, help_text="Enter a description of the room", verbose_name="Description")
    participants = models.ManyToManyField(User, related_name='participants', blank=True, help_text="Select participants for the room", verbose_name="Participants")
    updated = models.DateTimeField(auto_now=True, help_text="Time of the last update", verbose_name="Updated")
    created = models.DateTimeField(auto_now_add=True, help_text="Time the room was created", verbose_name="Created")

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Author of the message", verbose_name="User")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, help_text="Room where the message was sent", verbose_name="Room")
    body = models.TextField(help_text="Message text", verbose_name="Message")
    updated = models.DateTimeField(auto_now=True, help_text="Time the message was last updated", verbose_name="Updated")
    created = models.DateTimeField(auto_now_add=True, help_text="Time the message was created", verbose_name="Created")

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.body[0:50]
