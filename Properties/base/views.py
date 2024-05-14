from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .serializers import *

def home(request):
    # Apenas mostra as 4 propriedades mais recentes
    properties = Property.objects.order_by('-id')[:4]
    properties_with_images = []
    for prop in properties:
        # Obtém a primeira imagem da relação `images` (se houver)
        first_image = prop.images.first()  # Utiliza o `related_name` definido no modelo
        properties_with_images.append((prop, first_image))
    return render(request, 'home.html', {'properties_with_images': properties_with_images})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.profile_picture = form.cleaned_data.get('profile_picture')
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
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
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

# No caso do user
@login_required(redirect_field_name='next', login_url='/login/?next=add_property')
def add_property(request):
    # Check if the user is a 'host', redirect with an error message if not.
    if request.user.profile.user_type != 'host':
        messages.error(request, "Precisa estar autenticado como vendedor para adicionar uma propriedade.")
        return redirect('home')

    # Handle form submission.
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        image_form = PropertyImageForm(request.POST, request.FILES)

        # Validate forms before saving.
        if property_form.is_valid() and image_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.host = request.user.profile  # Set the host to the logged-in user's profile.
            property_instance.save()  # Save the property instance to the database.

            # Save each uploaded image file associated with the property.
            for uploaded_file in image_form.cleaned_data['images']:
                PropertyImage.objects.create(property=property_instance, image=uploaded_file)

            messages.success(request, "Property added successfully!")  # Success message for user feedback.
            return redirect('home')
    else:
        # Instantiate blank forms for GET request.
        property_form = PropertyForm()
        image_form = PropertyImageForm()

    # Render page with the property forms.
    return render(request, 'add_property.html', {
        'property_form': property_form,
        'image_form': image_form
    })


def property_details(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    average_rating = Review.objects.filter(host=property_obj.host).aggregate(average=Avg('rating'))
    average = average_rating['average']
    if average is None:
        average = "Sem rating"

    context = {
        'property': property_obj,
        'average_rating': average
    }

    return render(request, 'property_details.html', context)

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

@login_required
def delete_property_view(request, id):
    property = get_object_or_404(Property, pk=id, host__user=request.user)

    if request.method == 'POST':
        property.delete()
        messages.success(request, "Property successfully deleted.")
        return redirect('home')  # Redirect to a safe page after deletion

    context = {
        'property': property
    }
    return render(request, 'confirm_delete.html', context)


@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, pk=property_id, host__user=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            property = form.save()

            # Handle image uploads
            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(property=property, image=image)

            # Handle image deletions
            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                PropertyImage.objects.filter(id__in=delete_image_ids).delete()

            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=property.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PropertyForm(instance=property)

    images = PropertyImage.objects.filter(property=property)
    return render(request, 'edit_property.html', {'form': form, 'images': images})


@login_required
def create_review(request, host_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile
    if user_profile.user_type != 'guest':
        return redirect('home')

    host = get_object_or_404(Profile, pk=host_id, user_type='host')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.guest = user_profile
            review.host = host
            review.save()
            messages.success(request, 'Review atribuida com sucesso!')
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {'form': form})

def contactos(request):
    return render(request, 'contactos.html')

def my_properties(request, pk):
    user_obj = get_object_or_404(Profile, pk=pk)
    properties = Property.objects.filter(host=user_obj).order_by('-id')

    properties_with_images = []
    for prop in properties:
        # Obtém a primeira imagem da relação `images` (se houver)
        first_image = prop.images.first()  # Utiliza o `related_name` definido no modelo
        properties_with_images.append((prop, first_image))

    return render(request, 'my_properties.html', {'properties_with_images': properties_with_images})