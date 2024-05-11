from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField

from .models import Profile, Property, Message, Review


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    address = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        user_profile, created = Profile.objects.get_or_create(user=user)

        user_profile.address = self.cleaned_data['address']
        user_profile.phone_number = self.cleaned_data['phone_number']
        user_profile.user_type = self.cleaned_data['user_type']  # Aqui, atribuímos o user_type do formulário

        if commit:
            user_profile.save()

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
    class Meta:
        model = Property
        fields = ('title', 'description', 'location', 'price', 'area', 'num_bedrooms', 'num_bathrooms', 'elevator',
                  'parking_spaces', 'pool')


class PropertyImageForm(forms.Form):
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5)  # Máx. 10 arquivos, 5MB cada


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']  # Exclude 'host' from the form
        labels = {
            'rating': 'Rating',
            'review_text': 'Review Text',
        }

