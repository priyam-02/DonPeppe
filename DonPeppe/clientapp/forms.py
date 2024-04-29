from django import forms

from .models import booktable


class bookform(forms.ModelForm):
    class Meta:
        model = booktable
        fields = '__all__'