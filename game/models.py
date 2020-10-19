from django.db import models
from ndarray import NDArrayField
# Create your models here.

game_status = (
    (0, "Ongoing"),
    (-1, "Lost"),
    (1, "Won")
)

class user_info(models.Model):
    user_id = models.TextField(max_length= 12, unique= True, primary_key= True)

class board_info(models.Model):
    updated_on = models.DateTimeField(auto_now=True, null=True)
    user_id = models.ForeignKey(user_info, on_delete=None)
    true_board = NDArrayField()
    prob_board = NDArrayField(null= True)
    is_bot = models.BooleanField(default= False)
    to_give_board = NDArrayField()
    cell_left = models.IntegerField()
    number_bombs = models.IntegerField()
    timer = models.FloatField(null= True)
    status = models.IntegerField(choices= game_status, default= 0)
