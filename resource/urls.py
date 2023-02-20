from django.urls import  re_path
from . import views as core_views
from django.urls import path, include

urlpatterns = [
    path('resource/<int:pk>',core_views.resource_view,name="resource"),
    path('videos/<int:pk>',core_views.videos,name="videos"),
    re_path(r'^post/(?P<pk>[\w\@\.\/\-\_]+)/$',core_views.post_view,name='post'),
    path('translation/',core_views.fetch_translation,name="translation"),
    path('video_filter/<int:pk>/<str:style>/',core_views.video_filter,name='video_filter'),
]