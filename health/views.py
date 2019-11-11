from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Records
from users.models import Profile
from .forms import ReportForm
from .cancer_estimator import predict_cancer
from os import path


# Create your views here.

def report(request, title):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    cancer_prob = Records.objects.get(user=Profile.objects.get(user=request.user), title=title).cancer_prob
    context = {"cancer_prob": cancer_prob}
    return render(request, 'index/report.html', context)


def reports(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    context = {"records": Records.objects.all().filter(user=Profile.objects.get(user=request.user))}
    return render(request, 'index/reports.html', context=context)


def download(request, title):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    record = Records.objects.get(user=Profile.objects.get(user=request.user), title=title)
    req_file = record.filename()
    file_download = record.report
    if path.exists(record.report.path):
        response = HttpResponse(file_download.file, content_type="text/plain")
        return response


def upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("social:begin", args=["google-oauth2"]))
    form = ReportForm(request.POST or None, request.FILES or None)
    context = {"form": form, "error_message": ""}
    if form.is_valid():
        record = form.save(commit=False)
        record.title = record.title.replace(' ', '_')
        file_type = record.filename().split('.')[-1]
        if file_type != "txt":
            context = {'form': form, "error_message": "Unsupported File Format"}
            return render(request, 'index/upload.html', context)
        record.user = Profile.objects.get(user=request.user)
        repeat = Records.objects.all().filter(user=Profile.objects.get(user=request.user), title=record.title)
        print(repeat)
        if len(repeat) != 0:
            context = {'form': form, "error_message": "File with same title already exists"}
            return render(request, 'index/upload.html', context)
        record.save()
        updated_record = Records.objects.get(user=Profile.objects.get(user=request.user), title=record.title)
        updated_record.cancer_prob = predict_cancer(updated_record.report.path)
        updated_record.save()
        return HttpResponseRedirect(reverse('reports'))
    else:
        return render(request, 'index/upload.html', context)
