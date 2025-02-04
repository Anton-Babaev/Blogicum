from django.db import models

class Game(models.Model):
    """Модель игры."""
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания игры
    current_player = models.ForeignKey(
        'Player',
        null=True,
        on_delete=models.SET_NULL,
        related_name='current_of'
    )

class Player(models.Model):
    """Модель игрока."""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        'Game',
        related_name='players',
        on_delete=models.CASCADE
    )
    balance = models.IntegerField(default=1500)  # Начальный капитал
    position = models.IntegerField(default=0)  # Текущая позиция (0-19)

class Tile(models.Model):
    """Модель клетки игрового поля."""
    name = models.CharField(max_length=100)  # Название клетки
    type = models.CharField(
        max_length=50,
        choices=[
            ("start", "Старт"),
            ("jail", "Тюрьма"),
            ("treasury", "Казна"),
            ("free_parking", "Бесплатная парковка"),
            ("property", "Недвижимость"),
        ]
    )
    position = models.IntegerField(unique=True)  # Позиция на поле (0-19)