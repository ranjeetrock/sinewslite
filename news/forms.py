from django import forms
from .models import PatrakaarMitra

class PatrakaarMitraForm(forms.ModelForm):
    class Meta:
        model = PatrakaarMitra
        fields = ['name', 'mobile', 'email', 'gender', 'category', 'activity', 'address']
        widgets = {
            'activity': forms.Textarea(attrs={'rows': 2}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
