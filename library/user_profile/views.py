from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . models import UserProfile


@login_required
def view_profile(request):
    return render(request, 'user_profile/view_profile.html')
