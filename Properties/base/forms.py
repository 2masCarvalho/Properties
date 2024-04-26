from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    address = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = Profile.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
            )
        return user


class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # Exclude any other fields you don't want to be editable.


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone_number')
