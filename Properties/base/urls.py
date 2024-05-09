from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile, edit_profile, sobrenos
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('add_property/', views.add_property, name='add_property'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True, next_page=reverse_lazy('profile')), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('comprar/', views.buy, name='comprar'),
    path('vender/', views.sell, name='vender'),
    path('comprar/<int:pk>/', views.property_details, name='property_detail'),
    path('messages/', views.messages_view, name='messages'),
    path('sobrenos/', sobrenos, name='sobrenos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
