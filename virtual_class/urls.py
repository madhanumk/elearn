#from django.conf.urls import url
from . import views as v_views
from django.urls import path, include


urlpatterns = [   
    
    path('vtclass/',v_views.virtualclass,name="classroom"),
    path('topic/<int:pk>/',v_views.topic_view,name='topic'),
    path('topic_resource/<int:pk>/',v_views.topic_resources,name='topic_resource'), 
    path('assignment/<int:pk>/',v_views.assignment_view,name='assignment'),
    path('deleteassignment/<int:pk>/',v_views.delete_submission,name='join'),
    path('ask_questions/<int:pk>/',v_views.ask_questions,name='ask_questions'),
    path('view_discussion/<int:pk>/',v_views.view_discussion,name='view_discussion'), 
    path('view_replies/<int:pk>/',v_views.view_replies,name='view_replies'),
    path('vtclass/classroom_subject/<int:id>',v_views.classroom_subject,name="classroom_subject"),
    path('ajax_student_delete_submission/<int:pk>/',v_views.delete_submission,name='ajax_student_delete_submission'),
    path('ajax_load_assignment_charts/', v_views.draw_chart, name='ajax_load_assignment_charts'),   
]