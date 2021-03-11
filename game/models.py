from django.db import models
from ndarray import NDArrayField
# Create your models here.

game_status = (
    (0, "Ongoing"),
    (-1, "Lost"),
    (1, "Won")
)

game_type = (
    (1, "Easy"),
    (2, "Medium"),
    (3, "Hard")
)

class user_info(models.Model):
    user_id = models.TextField(max_length= 12, unique= True, primary_key= True)

class board_info(models.Model):
    updated_on = models.DateTimeField(auto_now=True, null=True)
    user_id = models.ForeignKey(user_info,null = True ,on_delete=models.SET_NULL)
    true_board = NDArrayField()
    prob_board = NDArrayField(null= True)
    is_bot = models.BooleanField(default= False)
    to_give_board = NDArrayField()
    cell_left = models.IntegerField()
    number_bombs = models.IntegerField()
    timer = models.FloatField(null= True)
    game_type = models.IntegerField(choices= game_type)
    status = models.IntegerField(choices= game_status, default= 0)
