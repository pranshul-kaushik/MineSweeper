from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .game_logic.opening_cells import new_board, update_board
from .models import board_info
import sys
sys.path.append(".")
from bot.AI import AI


import json
# Create your views here.


# def new_game(request):
#     game= board_info.objects.all()
#     for i in game:
#         i.delete()
#     return JsonResponse({})

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
    board, status = update_board(pos, action, user_id, time)
    return JsonResponse({"board": board.tolist(), "status": status, "user_id": user_id})

@csrf_exempt
def create_board(request):
    input_info =json.loads(request.body)
    num_row = int(input_info.get('num_row'))
    num_col = int(input_info.get('num_col'))
    user_id = input_info.get('user_id')
    board_info = new_board(num_row, num_col, user_id)
    _board_info = {'board':board_info.tolist()}
    return JsonResponse(_board_info,safe=False)
