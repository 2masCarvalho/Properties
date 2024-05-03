from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Property
#Library para possibilitar fazer upload de varias fotos
from multiupload.fields import MultiFileField

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    address = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    '''
    USER_ROLES = (
        ('user', 'User'),  # For regular users
        ('host', 'Host'),  # For hosts
    )
    role = forms.ChoiceField(choices=USER_ROLES, required=True, help_text='Are you signing up as a User or a Guest?')
    '''
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
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone_number', 'profile_picture')

class PropertyForm(forms.ModelForm):
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5)
    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'price']
