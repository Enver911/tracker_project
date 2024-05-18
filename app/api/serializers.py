from rest_framework import serializers
from tracker import models
from django.urls import reverse_lazy
from tracker.models import Board, Column, Card
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class BoardSerializer(serializers.ModelSerializer):
    
    def create(self, request, validated_data):
        instance = request.user.boards.create(**validated_data)
        return instance
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    class Meta:
        model = models.Board
        fields = ("id", "title", "description", "avatar", "background")
        
             
class CardSerializer(serializers.ModelSerializer):
    
    def create(self, column_id, validated_data):
        column = Column.objects.get(id=column_id)
        instance = Card.objects.create(**validated_data, column=column)
        return instance
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    class Meta:
        model = models.Card
        fields = ("id", "title", "description", "avatar", "background", "deadline")
        
        
class ColumnSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    def create(self, board_id, validated_data):
        board = Board.objects.get(id=board_id)
        instance = Column.objects.create(**validated_data, board=board)
        return instance
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    class Meta:
        model = models.Column
        fields = ("id", "title", "cards")
        

class UserSerializer(serializers.ModelSerializer):
    pass

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
        
        
