from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Player, Tile
import random

def start_game(request):
    """Начинает новую игру."""
    if not request.user.is_authenticated:
        return redirect('login')

    # Создаем новую игру и добавляем игрока
    game = Game.objects.create()
    player = Player.objects.create(user=request.user, game=game)

    return redirect('monopoly:game', game_id=game.id)

def game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    player = game.players.first()

    # Получаем все клетки игрового поля
    tiles = Tile.objects.order_by('position')

    # Генерация поля 6x6 с клетками только по периметру
    board = [[None] * 6 for _ in range(6)]

    # Верхняя сторона (клетки 0-5)
    for i in range(6):
        if i < len(tiles):
            board[0][i] = tiles[i]

    # Правая сторона (клетки 6-9)
    for i in range(1, 5):
        if 5 + i < len(tiles):
            board[i][5] = tiles[5 + i]

    # Нижняя сторона (клетки 10-15)
    for i in range(6):
        if 9 + i < len(tiles):  # Убедитесь, что здесь корректно используется индекс
            board[5][5 - i] = tiles[10 + i]

    # Левая сторона (клетки 16-19)
    for i in range(1, 5):
        if 15 + i < len(tiles):
            board[5 - i][0] = tiles[15 + i]

    # Определяем координаты игрока на поле
    player_position_in_board = None
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell and cell.position == player.position:
                player_position_in_board = (row_idx, col_idx)
                break

    return render(request, 'monopoly/game.html', {
        'game': game,
        'player': player,
        'board': board,
        'player_position_in_board': player_position_in_board,
    })

def roll_dice(request, game_id):
    """Обрабатывает бросок кубиков."""
    game = get_object_or_404(Game, id=game_id)
    player = game.players.first()

    # Бросаем кубики
    dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
    total_steps = dice1 + dice2

    # Обновляем позицию игрока
    player.position = (player.position + total_steps) % 20
    player.save()

    # Находим текущую клетку игрока
    current_tile = Tile.objects.get(position=player.position)

    # Генерация поля 6x6 с клетками только по периметру
    tiles = Tile.objects.order_by('position')
    board = [[None] * 6 for _ in range(6)]

    # Расположение клеток на поле
    for i in range(6):
        if i < len(tiles):
            board[0][i] = tiles[i]
    # Правая сторона (клетки 6-9)
    for i in range(1, 5):
        if 5 + i < len(tiles):
            board[i][5] = tiles[5 + i]
    # Нижняя сторона (клетки 10-15)
    for i in range(6):
        if 8 + i < len(tiles):
            board[5][5 - i] = tiles[10 + i]
    # Левая сторона (клетки 16-19)
    for i in range(1, 5):
        if 15 + i < len(tiles):
            board[5 - i][0] = tiles[15 + i]

    # Определяем координаты игрока на поле
    player_position_in_board = None
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell and cell.position == player.position:
                player_position_in_board = (row_idx, col_idx)
                break

    return render(request, 'monopoly/game.html', {
        'game': game,
        'player': player,
        'dice1': dice1,
        'dice2': dice2,
        'total_steps': total_steps,
        'current_tile': current_tile,
        'board': board,
        'player_position_in_board': player_position_in_board,
    })