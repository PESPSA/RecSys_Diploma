from django import forms
from django.core.exceptions import ValidationError

class createNewsform(forms.Form):
    abstract = forms.CharField(label='Абстрактное описание')
    subcategory = forms.CharField(label='Заголовок')
    body = forms.CharField(widget=forms.Textarea, label='Новость')