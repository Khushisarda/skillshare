from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import UserProfile, Skill


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    branch = forms.CharField(max_length=100, required=True)
    year = forms.CharField(max_length=10, required=True)
    college = forms.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "branch", "year", "college"]

    # remove help_texts (those extra messages)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # 👈 checkboxes
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'skills', 'profile_pic']