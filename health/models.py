from django.db import models
from users.models import Profile
from os import path


# Create your models here.

class Records(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    report = models.FileField(upload_to='reports/')
    cancer_prob = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def filename(self):
        return path.basename(self.report.name)
