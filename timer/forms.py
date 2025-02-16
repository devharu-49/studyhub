from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Times


class SaveTimeForm(ModelForm):
    class Meta:
        model = Times
        fields = ["count_time"]


# class LoginForm(forms.Form):
#     email = forms.EmailField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)