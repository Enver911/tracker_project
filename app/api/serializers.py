from rest_framework import serializers, validators
from tracker import models
from django.urls import reverse_lazy
from tracker.models import Board, Column, Card, Follower
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


class FollowerListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=get_user_model().objects.all())
    board = serializers.SlugRelatedField(slug_field="id", read_only=True)
    permission = serializers.ChoiceField(choices=Follower.Permissions.choices)
    
    def create(self, request, board_id):
        board = get_object_or_404(Board.objects, id=board_id)

        if board.followers.filter(user=self.validated_data["user"]).exists() or self.validated_data["user"] == request.user:
            raise serializers.ValidationError({"detail": "User already invited"})

        instance = board.followers.create(**self.validated_data)
        return instance
    
    class Meta:
        model = Follower
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    
    def create(self, request, card_id):
        card = get_object_or_404(Card.objects, id=card_id)
        
        if card.subscribers.filter(username=self.validated_data["username"]):
            raise serializers.ValidationError({"detail": "User already subscribed to the card"})
        
        author = card.column.board.author
        
        if author.username == self.validated_data["username"]:
            user = author
        else:
            user = get_object_or_404(card.column.board.followers, user__username=self.validated_data["username"]).user
        
        card.subscribers.add(user)
        
        return user
    
    class Meta:
        model = get_user_model()
        fields = ("id", "username")


class BoardSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    followers = FollowerListSerializer(many=True, read_only=True)
    
    def create(self, request):
        instance = request.user.boards.create(**self.validated_data)
        return instance
    
    def update(self, instance):
        for key, value in self.validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    class Meta:
        model = models.Board
        fields = ("id", "title", "description", "avatar", "background", "followers")
        
             
class CardSerializer(serializers.ModelSerializer):
    column = serializers.SlugRelatedField(slug_field="id", queryset=Column.objects.all(), required=False)
    avatar = serializers.ImageField(read_only=True)
    subscribers = SubscriberSerializer(many=True, read_only=True)
    
    def create(self, request, column_id):
        column = get_object_or_404(Column.objects, id=column_id)
        self.validated_data.pop("column", None)
        instance = column.cards.create(**self.validated_data)
        return instance
    
    def update(self, instance):
        for key, value in self.validated_data.items():
            setattr(instance, key, value)     
        instance.save()
        return instance
    
    class Meta:
        model = Card
        fields = ("id", "column", "title", "description", "avatar", "background", "foreground", "deadline", "subscribers")
        extra_kwargs = {"deadline": {"error_messages": {"invalid": "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DD hh:mm:ss"}}}
        
        
class ColumnSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    def create(self, request, board_id):
        board = get_object_or_404(Board.objects, id=board_id)
        instance = board.columns.create(**self.validated_data)
        return instance
    
    def update(self, instance):
        for key, value in self.validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    class Meta:
        model = models.Column
        fields = ("id", "title", "cards")
        

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass
    
    class Meta:
        model = get_user_model()
        fields = ()
        
        
        
class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    
    
class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    
    def create(self):
        instance = get_user_model().objects.create(username=self.validated_data["username"], 
                                                   email=self.validated_data["email"],
                                                   password=make_password(self.validated_data["password1"]))
        return instance
    
    def validate_username(self, username):
        user_check_username = get_user_model().objects.filter(username=username)
        if user_check_username:
            raise serializers.ValidationError("Username is already taken")
        return username
                
    def validate_email(self, email):
        user_check_email = get_user_model().objects.filter(email=email) 
        if user_check_email:
            raise serializers.ValidationError("Email is already taken")
        return email

    def validate(self, data):
        validate_password(data["password1"])
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("The entered passwords do not match")
        return data
        

        
        
class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    board = serializers.SlugRelatedField(slug_field="id", read_only=True)
    permission = serializers.ChoiceField(choices=Follower.Permissions.choices)
    
    def update(self, instance):
        for key, value in self.validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    class Meta:
        model = Follower
        fields = "__all__"


