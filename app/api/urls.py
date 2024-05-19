from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from api import views

app_name = "api"

urlpatterns = [
    # user api
    path("profile/", views.LoginView.as_view(), name="Profile"),
    path("login/", views.LoginView.as_view(), name="Login"),
    path("logout/", views.LogoutView.as_view(), name="Logout"),
    path("registration/", views.RegistrationView.as_view(), name="Registration"),
    
    # tracker api
    path("boards/", views.BoardListView.as_view(), name="BoardList"),
    path("boards/<int:board_id>/", views.BoardView.as_view(), name="Board"),
    path("boards/<int:board_id>/media/", views.BoardMediaView.as_view(), name="BoardMedia"),
    path("<int:board_id>/columns/", views.ColumnListView.as_view(), name="ColumnList"),
    path("columns/<int:column_id>/", views.ColumnView.as_view(), name="Column"),
    path("<int:column_id>/cards/", views.CardListView.as_view(), name="CardList"),
    path("cards/<int:card_id>/", views.CardView.as_view(), name="Card"),
    path("cards/<int:card_id>/media/", views.CardMediaView.as_view(), name="CardMedia"),
]
