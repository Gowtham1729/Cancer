from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Profile
from django.contrib.auth import logout


# Create your views here.
def home(request):
    return render(request, 'index/home.html')


@login_required()
def profile(request, user_handle):
    return render(request, 'index/profile.html')


@login_required()
def settings(request):
    profile_info = Profile.objects.get(user=request.user)
    context = {"profile_info": profile_info}
    return render(request, 'index/settings.html', context)

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
