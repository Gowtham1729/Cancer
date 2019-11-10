from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Records
from users.models import Profile
from .forms import ReportForm
from .cancer_estimator import predict_cancer
from os import path


# Create your views here.

@login_required()
def report(request, title):
    cancer_prob = Records.objects.get(user=Profile.objects.get(user=request.user), title=title).cancer_prob
    context = {"cancer_prob": cancer_prob}
    return render(request, 'index/report.html', context)


@login_required()
def reports(request):
    context = {"records": Records.objects.all().filter(user=Profile.objects.get(user=request.user))}
    return render(request, 'index/reports.html', context=context)


@login_required()
def download(request, title):
    record = Records.objects.get(user=Profile.objects.get(user=request.user), title=title)
    req_file = record.filename()
    file_download = record.report
    if path.exists(record.report.path):
        response = HttpResponse(file_download.file, content_type="text/plain")
        return response


@login_required()
def upload(request):
    form = ReportForm(request.POST or None, request.FILES or None)
    context = {"form": form}
    if form.is_valid():
        record = form.save(commit=False)
        record.user = Profile.objects.get(user=request.user)
        record.save()
        updated_record = Records.objects.get(user=Profile.objects.get(user=request.user), title=record.title)
        updated_record.cancer_prob = predict_cancer(updated_record.report.path)
        updated_record.save()
        return HttpResponseRedirect(reverse('reports'))
    else:
        return render(request, 'index/upload.html', context)
