from django.urls import  re_path
from . import views as core_views
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('test_view',views.test_view ,name="test"),
    path('chapter_list/<int:id>',views.chapter_list,name="chapter_list"),
    path('',core_views.CustomLoginView.as_view(), name='login',kwargs={'redirect_authenticated_user': True}),
    path('accounts/login/',core_views.CustomLoginView.as_view()),
    path('logout/',core_views.logout, name="logout"),
    path('home/',core_views.land_view,name="home"),
    path('my_profile/', core_views.edit_profile, name='my_profile'),
    path('dashboard/',core_views.dashboard,name='dashboard'),
    path('ajax/load_usage/', core_views.draw_usage, name='ajax_load_usage'),
    path('ajax/load_charts/', core_views.draw_chart, name='ajax_load_charts'),
    path('my_personality/',core_views.my_personality,name='my_personality'),    
]