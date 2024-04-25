from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sign-up/', views.createAccout, name="sign-up")
]