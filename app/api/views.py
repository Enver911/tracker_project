from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import BoardSerializer, ColumnSerializer, CardSerializer
from tracker.models import Column, Card
from django.shortcuts import get_object_or_404


# Create your views here.
class BoardListView(APIView):
    def get(self, request):
        boards = request.user.boards.all()
        serializer = BoardSerializer(instance=boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.create(request, serializer.validated_data)
            return Response(serializer.validated_data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BoardView(APIView):
    def put(self, request, board_id):
        instance = get_object_or_404(request.user.boards, id=board_id)        
        serializer = BoardSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.validated_data)
        
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
            serializer.create(board_id, serializer.validated_data)
            return Response(serializer.validated_data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ColumnView(APIView):
    def put(self, request, board_id, column_id):
        instance = get_object_or_404(Column.objects, board__id=board_id, id=column_id)
        serializer = ColumnSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.validated_data)
        
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
            serializer.create(column_id, serializer.validated_data)
            return Response(serializer.validated_data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CardView(APIView):
    def put(self, request, board_id, column_id, card_id):
        instance = get_object_or_404(Card.objects, column__id=column_id, id=card_id)
        serializer = CardSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.validated_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, board_id, column_id, card_id):
        instance = get_object_or_404(Card.objects, column__id=column_id, id=card_id)
        serializer = CardSerializer(instance=instance)
        data = serializer.data
        instance.delete()
        return Response(data)