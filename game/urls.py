from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_view, name='game'),  # For the main game page
    path('api/', views.game_api, name='game_api'),  # For handling AJAX requests
]
