from django.urls import path,include
from . import views as core_views

urlpatterns = [
    path('login/',core_views.LoginView.as_view(),name='login-api'),
    path('home/',core_views.HomeView.as_view(),name='api-home'),
  

    
]
