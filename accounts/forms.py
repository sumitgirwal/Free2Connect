from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import models
from .models import CustomUser, Interest

# Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone', 'gender', 'country', 'username', 'password1', 'password2', 'interests']
    
# Custom user login form
class CustomLoginForm(forms.Form):
    phone_or_email = forms.CharField(label='Phone or Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        phone_or_email = cleaned_data.get('phone_or_email')
        password = cleaned_data.get('password')

        if phone_or_email and password:
            # Check if the user exists with the provided phone or email
            user = CustomUser.objects.filter(models.Q(phone=phone_or_email) | models.Q(email=phone_or_email)).first()
            if user:
                # Authenticate the user with the provided password
                user = authenticate(request=self.request, username=user.username, password=password)
                if not user:
                    raise forms.ValidationError('Invalid phone/email or password.')
            else:
                raise forms.ValidationError('Invalid phone/email or password.')

        return cleaned_data

    def get_user(self):
        phone_or_email = self.cleaned_data.get('phone_or_email')
        user = CustomUser.objects.filter(models.Q(phone=phone_or_email) | models.Q(email=phone_or_email)).first()
        return user