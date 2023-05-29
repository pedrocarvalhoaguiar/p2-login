from django.shortcuts import render

from reward.models import Reward


def home(request):
    rewards = Reward.objects.exclude(reward__retrieved_by=request.user)
    return render(request, 'home.html', context={'rewards': rewards})
