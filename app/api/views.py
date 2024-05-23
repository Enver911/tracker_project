from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import (BoardSerializer, 
                             ColumnSerializer, 
                             CardSerializer, 
                             AuthSerializer, 
                             RegistrationSerializer, 
                             FollowerSerializer, 
                             FollowerListSerializer, 
                             SubscriberSerializer,
                             ProfileSerializer)
from api.forms import AvatarForm
from tracker.models import Board, Column, Card, Follower
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication 
from rest_framework.authtoken.models import Token
from api import permissions


# Create your views here.
class BoardListView(APIView):
    def get(self, request):
        boards = Board.objects.filter(Q(author=request.user) | Q(followers__user=request.user))
        serializer = BoardSerializer(instance=boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.create(request)
            serializer_info = BoardSerializer(instance=instance_info)
            return Response(serializer_info.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BoardView(APIView):
    permission_classes = (permissions.BoardPermission, )
    def get(self, request, board_id):
        instance = get_object_or_404(Board.objects, id=board_id)
        serializer = BoardSerializer(instance=instance)
        return Response(serializer.data)
    
    def put(self, request, board_id):
        instance = get_object_or_404(Board.objects, id=board_id)        
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance)
            serializer_info = BoardSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, board_id):
        instance = get_object_or_404(Board.objects, id=board_id)
        serializer = BoardSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    

class ColumnListView(APIView):
    def get(self, request, board_id):
        columns = Column.objects.filter(board__id=board_id)
        serializer = ColumnSerializer(instance=columns, many=True)
        return Response(serializer.data)
    
    def post(self, request, board_id):
        serializer = ColumnSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.create(request, board_id)
            serializer_info = ColumnSerializer(instance=instance_info)
            return Response(serializer_info.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColumnView(APIView):
    def get(self, request, column_id):
        instance = get_object_or_404(Column.objects, id=column_id)
        serializer = ColumnSerializer(instance=instance)
        return Response(serializer.data)
    
    
    def put(self, request, column_id):
        instance = get_object_or_404(Column.objects, id=column_id)
        serializer = ColumnSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance)
            serializer_info = ColumnSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, column_id):
        instance = get_object_or_404(Column.objects, id=column_id)
        serializer = ColumnSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    
    
class CardListView(APIView):
    def get(self, request, column_id):
        cards = Card.objects.filter(column__id=column_id)
        serializer = CardSerializer(instance=cards, many=True)
        return Response(serializer.data)
    
    def post(self, request, column_id):
        serializer = CardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.create(request, column_id)
            serializer_info = CardSerializer(instance=instance_info)
            return Response(serializer_info.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CardView(APIView):
    def get(self, request, card_id):
        instance = get_object_or_404(Card.objects, id=card_id)
        serializer = CardSerializer(instance=instance)
        return Response(serializer.data)
    
    def put(self, request, card_id):
        instance = get_object_or_404(Card.objects, id=card_id)
        serializer = CardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance)
            serializer_info = CardSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, card_id):
        instance = get_object_or_404(Card.objects, id=card_id)
        serializer = CardSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    
    
class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():  
            serializer.create()
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data["username"], password=serializer.validated_data["password"])
            
            if user:
                login(request, user)
                Token.objects.filter(user=user).delete() # delete old tokens every login
                new_token = Token.objects.create(user=user) # return new token
                return Response({"Token": f"{str(new_token)}"})
            
            return Response({"detail": "Wrong username or password"}, status=status.HTTP_403_FORBIDDEN)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        Token.objects.filter(user=request.user).delete() # delete old tokens every login
        logout(request)
        return Response({"detail": "Logged out"})


class BoardMediaView(APIView):
    def put(self, request, board_id):
        instance = get_object_or_404(Board.objects, id=board_id)  
        form = AvatarForm(files=request.FILES)
        
        if form.is_valid():
            form.save(instance=instance)
            return Response({"detail": "Data was saved"})
        
        return Response({"detail": "Wrong data"}, status=status.HTTP_400_BAD_REQUEST)


class CardMediaView(APIView):
    def put(self, request, card_id):
        instance = get_object_or_404(Card.objects, id=card_id)
        form = AvatarForm(files=request.FILES)
        
        if form.is_valid():
            form.save(instance=instance)
            return Response({"detail": "Data was saved"})
        
        return Response({"detail": "Wrong data"}, status=status.HTTP_400_BAD_REQUEST)
   
    

class BoardFollowerListView(APIView):
    def get(self, request, board_id):
        followers = Follower.objects.filter(board__id=board_id)
        serializer = FollowerListSerializer(instance=followers, many=True)
        return Response(serializer.data)    
    
    def post(self, request, board_id):
        serializer = FollowerListSerializer(data=request.data)       
        
        if serializer.is_valid():
            instance_info = serializer.create(request, board_id)
            serializer_info = FollowerListSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class BoardFollowerView(APIView):
    def put(self, request, follower_id):
        instance = get_object_or_404(Follower.objects, id=follower_id)
        serializer = FollowerSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance)
            serializer_info = FollowerSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, follower_id):
        instance = get_object_or_404(Follower.objects, id=follower_id)
        serializer = FollowerSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    

class SubscriberListView(APIView):
    def get(self, request, board_id, card_id):
        subscribers = get_object_or_404(Card.objects, id=card_id).subscribers
        serializer = SubscriberSerializer(instance=subscribers, many=True)
        return Response(serializer.data)
    
    def post(self, request, board_id, card_id):
        serializer = SubscriberSerializer(data=request.data)       
        
        if serializer.is_valid():
            instance_info = serializer.create(request, card_id)
            serializer_info = SubscriberSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class SubscriberView(APIView):

    def delete(self, request, board_id, card_id, user_id):
        card = get_object_or_404(Card.objects, id=card_id)
        instance = get_object_or_404(card.subscribers, id=user_id)
        serializer = SubscriberSerializer(instance=instance)
        data = serializer.data
        card.subscribers.remove(instance)
        return Response(data)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        instance = request.user
        serializer = ProfileSerializer(instance=instance)
        return Response(serializer.data)
    
    def put(self, request):
        instance = request.user
        serializer = ProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance)
            serializer_info = ProfileSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileMediaView(APIView):
    def put(self, request):
        instance = request.user
        form = AvatarForm(files=request.FILES)
        
        if form.is_valid():
            form.save(instance=instance)
            return Response({"detail": "Data was saved"})
        
        return Response({"detail": "Wrong data"}, status=status.HTTP_400_BAD_REQUEST)