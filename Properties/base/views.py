from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm, CustomUserChangeForm, PropertyImageForm, PropertyForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .models import Profile, Property, PropertyImage
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # Atenção ao request.FILES aqui
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'edit_profile.html', context)

def buy(request):
    properties = Property.objects.order_by('-id')

    properties_with_images = []
    for prop in properties:
        # Obtém a primeira imagem da relação `images` (se houver)
        first_image = prop.images.first()  # Utiliza o `related_name` definido no modelo
        properties_with_images.append((prop, first_image))

    return render(request, 'buy.html', {'properties_with_images': properties_with_images})

def sell(request):
    return render(request, 'sell.html')

'''
@login_required
def add_property(request):
    if request.user.profile.user_type == 'host':
        if request.method == 'POST':
            form = PropertyForm(request.POST)
            if form.is_valid():
                property = form.save(commit=False)
                property.host = request.user.profile
                property.save()
                return redirect('home') #add the url do the property details
        else:
            form = PropertyForm()
        return render(request, 'add_property.html', {'form': form})
    else:
        return redirect('home')
        
'''
@login_required
def add_property(request):
    if request.user.profile.user_type == 'host':
        if request.method == 'POST':
            property_form = PropertyForm(request.POST)
            image_form = PropertyImageForm(request.POST, request.FILES)

            if property_form.is_valid() and image_form.is_valid():
                property_instance = property_form.save(commit=False)
                property_instance.host = request.user.profile
                property_instance.save()

                for uploaded_file in image_form.cleaned_data['images']:
                    PropertyImage.objects.create(property=property_instance, image=uploaded_file)

                return redirect('home')
        else:
            property_form = PropertyForm()
            image_form = PropertyImageForm()

        return render(request, 'add_property.html', {'form': property_form, 'image_form': image_form})
    else:
        return redirect('home')