from django.shortcuts import render

from reward.models import Reward


def home(request):
    if request.user.is_authenticated:
        rewards = Reward.objects.exclude(reward__retrieved_by=request.user)
    else:
        rewards = Reward.objects.all()
    return render(request, 'home.html', context={'rewards': rewards})
