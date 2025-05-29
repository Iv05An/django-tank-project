from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Comment

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email







class CommentForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Ваше имя", widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}))
    content = forms.CharField(label="Комментарий", widget=forms.Textarea(attrs={'placeholder': 'Ваш комментарий', 'rows': 3}))

    class Meta:
        model = Comment
        fields = ['username', 'content']