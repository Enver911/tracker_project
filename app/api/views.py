from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import BoardSerializer, ColumnSerializer, CardSerializer, AuthSerializer, RegistrationSerializer
from api.forms import BoardForm, CardForm
from tracker.models import Column, Card
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication 
from rest_framework.authtoken.models import Token

# Create your views here.
class BoardListView(APIView):
    
    def get(self, request):
        boards = request.user.boards.all()
        serializer = BoardSerializer(instance=boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.create(request, serializer.validated_data)
            serializer_info = BoardSerializer(instance=instance_info)
            return Response(serializer_info.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BoardView(APIView):
    
    def put(self, request, board_id):
        instance = get_object_or_404(request.user.boards, id=board_id)        
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance, serializer.validated_data)
            serializer_info = BoardSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, board_id):
        instance = get_object_or_404(request.user.boards, id=board_id)
        serializer = BoardSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    
class ColumnListView(APIView):
    
    def get(self, request, board_id):
        columns = Column.objects.filter(board__id=board_id).all()
        serializer = ColumnSerializer(instance=columns, many=True)
        return Response(serializer.data)
    
    def post(self, request, board_id):
        serializer = ColumnSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.create(board_id, serializer.validated_data)
            serializer_info = ColumnSerializer(instance=instance_info)
            return Response(serializer_info.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ColumnView(APIView):
    
    def put(self, request, board_id, column_id):
        instance = get_object_or_404(Column.objects, board__id=board_id, id=column_id)
        serializer = ColumnSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance, serializer.validated_data)
            serializer_info = ColumnSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, board_id, column_id):
        instance = get_object_or_404(Column.objects, board__id=board_id, id=column_id)
        serializer = ColumnSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    
class CardListView(APIView):
    
    def get(self, request, board_id, column_id):
        cards = Card.objects.filter(column__id=column_id).all()
        serializer = CardSerializer(instance=cards, many=True)
        return Response(serializer.data)
    
    def post(self, request, board_id, column_id):
        serializer = CardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.create(column_id, serializer.validated_data)
            serializer_info = CardSerializer(instance=instance_info)
            return Response(serializer_info.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CardView(APIView):
    def put(self, request, board_id, column_id, card_id):
        instance = get_object_or_404(Card.objects, column__id=column_id, id=card_id)
        serializer = CardSerializer(data=request.data)
        
        if serializer.is_valid():
            instance_info = serializer.update(instance, serializer.validated_data)
            serializer_info = CardSerializer(instance=instance_info)
            return Response(serializer_info.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, board_id, column_id, card_id):
        instance = get_object_or_404(Card.objects, column__id=column_id, id=card_id)
        serializer = CardSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)
    
    
class RegistrationView(APIView):
    def post(self, request):
        pass
    
    
class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():  
            get_user_model().objects.create(username=serializer.validated_data["username"], 
                                            email=serializer.validated_data["email"], 
                                            password=make_password(serializer.validated_data["password1"]))
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
    def post(self, request):
        Token.objects.filter(user=request.user).delete() # delete old tokens every login
        logout(request)
        return Response({"detail": "Logged out"})


class BoardMediaView(APIView):
    def put(self, request, board_id):
        instance = get_object_or_404(request.user.boards, id=board_id)  
        form = BoardForm(files=request.FILES)
        
        if form.is_valid():
            form.save(instance=instance)
            return Response({"detail": "Data was saved"})
        
        return Response({"detail": "Wrong data"}, status=status.HTTP_400_BAD_REQUEST)


class CardMediaView(APIView):
    def put(self, request, board_id, column_id, card_id):
        instance = get_object_or_404(Card.objects, column__id=column_id, id=card_id)
        form = CardForm(files=request.FILES)
        
        if form.is_valid():
            form.save(instance=instance)
            return Response({"detail": "Data was saved"})
        
        return Response({"detail": "Wrong data"}, status=status.HTTP_400_BAD_REQUEST)
    
