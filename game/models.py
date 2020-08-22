from django.db import models
from ndarray import NDArrayField
# Create your models here.

class board_info(models.Model):
    true_board = NDArrayField()
    # prob_board
    # is bot
    to_give_board = NDArrayField()
    cell_left = models.IntegerField()
    number_bombs = models.IntegerField()

#user table
#leader board