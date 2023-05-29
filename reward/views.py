from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from reward.models import Reward, ReceivedReward


@login_required(login_url='/login')
def mec_reward(request, pk):
    reward = Reward.objects.filter(id=pk).first()
    user = request.user
    if reward.points_needed <= user.points and not ReceivedReward.objects.filter(reward_id=reward.id, retrieved_by_id=user.id):
        ReceivedReward.objects.create(reward=reward, retrieved_by=request.user)
        user.points -= reward.points_needed
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Recompensa resgatada!')
    else:
        messages.add_message(request, messages.WARNING, 'Pontos insuficientes')
    return redirect('home')
