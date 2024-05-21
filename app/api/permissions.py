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
        
        author = None
        
        board_id = view.kwargs.get("board_id")
        column_id = view.kwargs.get("column_id")
        card_id = view.kwargs.get("card_id")   
        follower_id = view.kwargs.get("follower_id")
        
        if board_id:
            author = get_object_or_404(models.Board.objects, id=board_id).author
        elif column_id:
            author = get_object_or_404(models.Column.objects, id=column_id).board.author
        elif card_id:
            author = get_object_or_404(models.Card.objects, id=card_id).column.board.author
        elif follower_id:
            author = get_object_or_404(models.Follower.objects, id=follower_id).board.author
            
        if request.user and request.user.is_authenticated and author and author == request.user:
            return True
        
        return False
    
    
class FUCKINGPERMISSION(BasePermission):

    def has_permission(self, request, view):
        
        author = request.user
        follower = None
        
        board_id = view.kwargs.get("board_id")
        column_id = view.kwargs.get("column_id")
        card_id = view.kwargs.get("card_id")   
        follower_id = view.kwargs.get("follower_id")
        
        print(board_id, column_id, card_id, follower_id)
        
        if board_id:
            author = get_object_or_404(models.Board.objects, id=board_id).author
            follower = models.Board.objects.get(id=board_id).followers.filter(user=request.user)

        elif column_id:
            author = get_object_or_404(models.Column.objects, id=column_id).board.author
            follower = models.Column.objects.get(id=column_id).board.followers.filter(user=request.user)

        elif card_id:
            author = get_object_or_404(models.Card.objects, id=card_id).column.board.author
            follower = models.Card.objects.get(id=card_id).column.board.followers.filter(user=request.user)

        elif follower_id:
            author = get_object_or_404(models.Follower.objects, id=follower_id).board.author
            follower = models.Follower.objects.filter(id=follower_id).filter(user=request.user)
            
        follower = follower.first() if follower and follower.exists() else None
            
        if request.method in SAFE_METHODS:
            if (request.user and request.user.is_authenticated and 
            ((author and author == request.user) or 
             (follower and follower.user == request.user))):
                return True
        else:
            if (request.user and request.user.is_authenticated and 
            ((author and author == request.user) or 
             (follower and follower.user == request.user and follower.permission == models.Follower.Permissions.MODERATOR))):
                return True
        
        return False