from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .game_logic.opening_cells import new_board, update_board
from .models import board_info

import json
# Create your views here.


def new_game(request):
    game= board_info.objects.all()
    for i in game:
        #print(i)
        i.delete()
    return JsonResponse({})


@csrf_exempt
def play_board(request):
    input_info =json.loads(request.body)
    num_row = int(input_info.get('num_row'))
    num_col = int(input_info.get('num_col'))
    pos = (num_row,num_col)
    action = int(input_info.get('action'))
    #print(action)
    board, status = update_board(pos, action)
    return JsonResponse({"board": board.tolist(), "status": status})

@csrf_exempt
def create_board(request):
    input_info =json.loads(request.body)
    num_row = int(input_info.get('num_row'))
    num_col = int(input_info.get('num_col'))
    board_info = new_board(num_row, num_col)
    _board_info = {'board':board_info.tolist()}
    return JsonResponse(_board_info,safe=False)
