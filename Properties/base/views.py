from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import SignUpForm, ProfileForm, CustomUserChangeForm, PropertyImageForm, PropertyForm, MessageForm
from .models import Profile, Property, PropertyImage, Message
from django.contrib.auth.models import User



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
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)  # Atenção ao request.FILES aqui
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


@login_required
def add_property(request):
    # Check if the user is a 'host'
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
        # Redirect to the home page with a temporary message
        messages.info(request, "You need to be logged in as a host to add a property.")
        return redirect('home')


def property_details(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'property_details.html', {'property': property_obj})

def messages_view(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user from the list of conversations
    selected_user = None
    conversation = []

    if 'user' in request.GET:
        selected_user = get_object_or_404(User, id=request.GET['user'])
        conversation = Message.objects.filter(
            sender=request.user, receiver=selected_user
        ) | Message.objects.filter(
            sender=selected_user, receiver=request.user
        )
        conversation = conversation.order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver_id = request.POST['receiver']
            message.save()
    else:
        form = MessageForm()

    return render(request, 'messages.html', {
        'users': users,
        'selected_user': selected_user,
        'conversation': conversation,
        'form': form,
    })

def sobrenos(request):
    return render(request, 'sobrenos.html')