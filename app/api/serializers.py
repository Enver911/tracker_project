from rest_framework import serializers
from tracker import models
from django.urls import reverse_lazy
from tracker.models import Board, Column, Card
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class BoardSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(allow_null=True, max_length=100, required=False, read_only=True)
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
        fields = ("id", "title", "description", "avatar", "background")
        
             
class CardSerializer(serializers.ModelSerializer):
    column = serializers.SlugRelatedField(slug_field="id", queryset=Column.objects.all(), required=False)
    avatar = serializers.ImageField(allow_null=True, max_length=100, required=False, read_only=True)
    
    def create(self, column_id):
        column = Column.objects.get(id=column_id)
        instance = Card.objects.create(**self.validated_data, column=column)
        return instance
    
    def update(self, instance):
        for key, value in self.validated_data.items():
            setattr(instance, key, value)     
        instance.save()
        return instance
    
    class Meta:
        model = models.Card
        fields = ("id", "column", "title", "description", "avatar", "background", "foreground", "deadline")
        extra_kwargs = {"deadline": {"error_messages": {"invalid": "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DD hh:mm:ss"}}}
        
        
class ColumnSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    def create(self, board_id):
        board = Board.objects.get(id=board_id)
        instance = Column.objects.create(**self.validated_data, board=board)
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
        
        
