from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from api import views

app_name = "api"

urlpatterns = [
    path('boards/', views.BoardListView.as_view(), name="BoardList"),
    path('boards/<int:board_id>/', views.BoardView.as_view(), name="Board"),
    path('boards/<int:board_id>/columns/', views.ColumnListView.as_view(), name="ColumnList"),
    path('boards/<int:board_id>/columns/<int:column_id>/', views.ColumnView.as_view(), name="Column"),
    path('boards/<int:board_id>/columns/<int:column_id>/cards/', views.CardListView.as_view(), name="CardList"),
    path('boards/<int:board_id>/columns/<int:column_id>/cards/<int:card_id>/', views.CardView.as_view(), name="Card"),
]
