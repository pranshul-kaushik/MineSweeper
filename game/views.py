from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .game_logic.opening_cells import new_board, update_board
from .models import board_info
import sys
sys.path.append(".")
from bot.AI import AI
from django.db import transaction


import json

@csrf_exempt
def bot(request):
    input_info = json.loads(request.body)
    user_id = input_info.get('user_id')
    time = float(input_info.get('timer'))
    num_row, num_col, action, status, board =  AI(user_id, time)
    return JsonResponse({"board": board.tolist(), "status": status, "user_id": user_id,
                         "num_row": num_row, "num_col": num_col, "action": action})

@csrf_exempt
def play_board(request):
    input_info =json.loads(request.body)
    num_row = int(input_info.get('num_row'))
    num_col = int(input_info.get('num_col'))
    user_id = input_info.get('user_id')
    pos = (num_row,num_col)
    action = int(input_info.get('action'))
    time = float(input_info.get('timer'))
    try:
        with transaction.atomic():
            board,given_board, status, action = update_board(pos, action, user_id, time)

            return JsonResponse({"board": given_board.tolist(),
                         "status": status, 
                         "user_id": user_id, 
                         "num_row": num_row, 
                         "num_col": num_col, 
                         "action": action
                         })
    except:
        print("Fast Click! Data Base Locked")
        return JsonResponse({"message": "Wait"}, status = 401)

@csrf_exempt
def create_board(request):
    input_info =json.loads(request.body)
    num_row = int(input_info.get('num_row'))
    num_col = int(input_info.get('num_col'))
    user_id = input_info.get('user_id')
    bot = bool(input_info.get('is_bot'))
    game_type = int(input_info.get('game_type'))
    board_info, number_bombs = new_board(num_row, num_col, user_id, bot, game_type)
    _board_info = {'board':board_info.tolist(), 'number_bombs': number_bombs}
    return JsonResponse(_board_info,safe=False)

@csrf_exempt
def show_highscore(request):
    return JsonResponse({"high_score":list(board_info.objects.filter(status = 1, is_bot= False).order_by("timer").values("user_id", "game_type", "timer"))})
