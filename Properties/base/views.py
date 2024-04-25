from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'home.html')


def createAccout(request):
    return render(request, 'sign-up.html')
