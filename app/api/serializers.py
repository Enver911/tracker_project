from rest_framework import serializers
from tracker import models
from django.urls import reverse_lazy
from tracker.models import Board, Column, Card


class BoardSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(required=False)
    
    def get_url(self, obj):
        return reverse_lazy("api:Board", kwargs={"board_id": obj.id})
    
    def create(self, request, validated_data):
        instance = request.user.boards.create(title=validated_data["title"])
        return instance
    
    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.save()
        return instance
    
    class Meta:
        model = models.Board
        fields = ("title", "url")
        
class ColumnSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(required=False)
    
    def get_url(self, obj):
        return reverse_lazy("api:Column", kwargs={"board_id": obj.board.id, 
                                                  "column_id": obj.id})
    
    def create(self, board_id, validated_data):
        board = Board.objects.get(id=board_id)
        instance = Column.objects.create(title=validated_data["title"], board=board)
        return instance
    
    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.save()
        return instance
    
    class Meta:
        model = models.Column
        fields = ("title", "url")
        
class CardSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(required=False)
    
    def get_url(self, obj):
        return reverse_lazy("api:Card", kwargs={"board_id": obj.column.board.id, 
                                                  "column_id": obj.column.id, 
                                                  "card_id": obj.id})
    
    def create(self, column_id, validated_data):
        column = Column.objects.get(id=column_id)
        instance = Card.objects.create(title=validated_data["title"], column=column)
        return instance
    
    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.save()
        return instance
    
    class Meta:
        model = models.Card
        fields = ("title", "url")