from rest_framework.permissions import BasePermission, SAFE_METHODS
from tracker import models
from django.shortcuts import get_object_or_404

class IsAuthorModerOrReadOnly(BasePermission):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
    
class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        
        board_author = None
        
        board_id = view.kwargs.get("board_id")
        column_id = view.kwargs.get("column_id")
        card_id = view.kwargs.get("card_id")   
        follower_id = view.kwargs.get("follower_id")
        
        if board_id:
            board_author = get_object_or_404(models.Board.objects, id=board_id).board_author
        elif column_id:
            board_author = get_object_or_404(models.Column.objects, id=column_id).board.board_author
        elif card_id:
            board_author = get_object_or_404(models.Card.objects, id=card_id).column.board.board_author
        elif follower_id:
            board_author = get_object_or_404(models.Follower.objects, id=follower_id).board.board_author
            
        if request.user and request.user.is_authenticated and board_author and board_author == request.user:
            return True
        
        return False
    
    
class BoardPermission(BasePermission): # only author can send DELETE queries

    def has_permission(self, request, view):
        
        if not (request.user and request.user.is_authenticated):
            return False
        
        board_author = None if view.kwargs else request.user
        board_follower = None
        
        board_id = view.kwargs.get("board_id")
        column_id = view.kwargs.get("column_id")
        card_id = view.kwargs.get("card_id")   
        follower_id = view.kwargs.get("follower_id")
        
        if board_id:
            board_author = get_object_or_404(models.Board.objects, id=board_id).author
            board_follower = models.Board.objects.get(id=board_id).followers.filter(user=request.user)

        elif column_id:
            board_author = get_object_or_404(models.Column.objects, id=column_id).board.author
            board_follower = models.Column.objects.get(id=column_id).board.followers.filter(user=request.user)

        elif card_id:
            board_author = get_object_or_404(models.Card.objects, id=card_id).column.board.author
            board_follower = models.Card.objects.get(id=card_id).column.board.followers.filter(user=request.user)

        elif follower_id:
            board_author = get_object_or_404(models.Follower.objects, id=follower_id).board.author
            board_follower = models.Follower.objects.filter(id=follower_id).filter(user=request.user)
             
        board_follower = board_follower.first() if board_follower and board_follower.exists() else None
            
        if request.method in SAFE_METHODS:
            if ((board_author and board_author == request.user) or 
             (board_follower and board_follower.user == request.user)):
                return True
        elif request.method == "DELETE":
            if board_author and board_author == request.user:
                return True
        else:
            if ((board_author and board_author == request.user) or 
             (board_follower and board_follower.user == request.user and board_follower.permission == models.Follower.Permissions.MODERATOR)):
                return True
        
        return False
    
class CommonPermission(BasePermission):

    def has_permission(self, request, view):
        
        if not (request.user and request.user.is_authenticated):
            return False
        
        board_author = None if view.kwargs else request.user
        board_follower = None
        
        board_id = view.kwargs.get("board_id")
        column_id = view.kwargs.get("column_id")
        card_id = view.kwargs.get("card_id")   
        follower_id = view.kwargs.get("follower_id")
        
        if board_id:
            board_author = get_object_or_404(models.Board.objects, id=board_id).author
            board_follower = models.Board.objects.get(id=board_id).followers.filter(user=request.user)

        elif column_id:
            board_author = get_object_or_404(models.Column.objects, id=column_id).board.author
            board_follower = models.Column.objects.get(id=column_id).board.followers.filter(user=request.user)

        elif card_id:
            board_author = get_object_or_404(models.Card.objects, id=card_id).column.board.author
            board_follower = models.Card.objects.get(id=card_id).column.board.followers.filter(user=request.user)

        elif follower_id:
            board_author = get_object_or_404(models.Follower.objects, id=follower_id).board.author
            board_follower = models.Follower.objects.filter(id=follower_id).filter(user=request.user)
             
        board_follower = board_follower.first() if board_follower and board_follower.exists() else None
            
        if request.method in SAFE_METHODS:
            if ((board_author and board_author == request.user) or 
             (board_follower and board_follower.user == request.user)):
                return True
        else:
            if ((board_author and board_author == request.user) or 
             (board_follower and board_follower.user == request.user and board_follower.permission == models.Follower.Permissions.MODERATOR)):
                return True
        
        return False
    
