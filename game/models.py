from django.db import models
from ndarray import NDArrayField
# Create your models here.

class user_info(models.Model):
    user_id = models.TextField(max_length= 12, unique= True, primary_key= True)

class board_info(models.Model):
    user_id = models.ForeignKey(user_info, on_delete=None)
    true_board = NDArrayField()
    # prob_board
    # is bot
    to_give_board = NDArrayField()
    cell_left = models.IntegerField()
    number_bombs = models.IntegerField()
    timer = models.FloatField(null= True)
