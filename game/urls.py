from django.urls import path
from .views import * 

urlpatterns = [
    path('update_board/',play_board),
    path('create_board/', create_board),
    path('bot/', bot),
    path('high_score/', show_highscore)

]