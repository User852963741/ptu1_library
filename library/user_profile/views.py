from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from . forms import UserUpdateForm, UserProfileUpdateForm


@login_required
def view_profile(request):
    return render(request, 'user_profile/view_profile.html')


@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Vartotojo {request.user} duomenys atnaujinti')
            return redirect('view_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.user_profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user_profile/edit_profile.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # duomenu surinkimas
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # validuosim forma, tikrindami ar sutampa slaptažodžiai, ar egzistuoja vartotojas
        error = False
        if not password or password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa arba neįvesti.')
            error = True
        if not username or User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojas {username} jau egzistuoja arba neįvestas.')
            error = True
        if not email or User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el.praštu {email} jau egzistuoja arba neįvestas.')
            error = True
        if error:
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'Vartotojas {username} užregistruotas sėkmingai. Galite prisijungti')
            return redirect('index')
    return render(request, 'user_profile/register.html')
