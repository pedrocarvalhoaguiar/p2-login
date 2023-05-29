from django.db import models

from user.models import CustomUser


class Reward(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    points_needed = models.IntegerField()


class ReceivedReward(models.Model):
    reward = models.ForeignKey(Reward, related_name='reward', on_delete=models.DO_NOTHING)
    retrieved_by = models.ForeignKey(CustomUser, related_name='received_by', on_delete=models.DO_NOTHING)
    retrieved_at = models.DateTimeField(auto_now_add=True)

