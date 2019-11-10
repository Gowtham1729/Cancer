from django import forms
from .models import Records


class ReportForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = ['title', 'report']