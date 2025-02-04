from django.urls import path
from . import views

app_name = 'monopoly'

urlpatterns = [
    path('start/', views.start_game, name='start_game'),  # Начало игры
    path('roll/<int:game_id>/', views.roll_dice, name='roll_dice'),  # Бросить кубики
    path('game/<int:game_id>/', views.game_view, name='game'),  # Маршрут для самой игры

]