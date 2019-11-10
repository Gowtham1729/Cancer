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


def profile(request, user_handle):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    return render(request, 'index/profile.html')


def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    profile_info = Profile.objects.get(user=request.user)
    context = {"profile_info": profile_info}
    return render(request, 'index/settings.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    logout(request)
    return HttpResponseRedirect(reverse('home'))
