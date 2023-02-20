#from django.conf.urls import url
#from django.conf.urls import url
from . import views
from django.urls import path, include

urlpatterns = [   
    path('college_admin',views.college_admin ,name="college_admin"),
    #path('school_admin',views.school_admin ,name="school"),
    path('ajax_get_student',views.ajax_get_student ,name="ajax_get_student"),
    path('student_datail/<int:pk>',views.student_datail,name="student_datail"),  


    path('students/',views.students_list,name="students"), 
    path('faculty/',views.faculty_list,name="faculty"), 
    path('logbook-history/<int:pk>',views.logbook_history,name="logbook-history"), 
    path('user_edit/<str:role>/<int:pk>',views.user_edit,name="user_edit"),
    path('view_teacher/<int:pk>',views.view_teacher,name="view_teacher"),
    path('remove_subject/<int:pk>',views.remove_subject,name="remove_subject"),
    path('teacher_subject_load/<str:grade>',views.teacher_subject_load,name="teacher_subject_load"),
    path('subject_assignment/<int:pk>',views.subject_assignment,name="subject_assignment"),
    path('subject_report/<int:pk>/<int:subject>',views.subject_report,name="subject_report"),
    #Post
    path('view_post/',views.view_post,name="view_post"),
    path('post_add/',views.post_add,name="post_add"),
    path('post_edit/<int:pk>',views.post_edit,name="post_edit"),
    path('post_delete/<int:pk>',views.post_delete,name="post_delete"),
    path('password_reset/<int:pk>',views.password_reset,name="password_reset"),

    #Score
    path('score/',views.score,name="score"),

    path('subject-load/',views.subject_load,name="subject-load"),    
    #path('view_subjects/<str:grade>/<str:section>',views.view_subjects,name="view_subjects"),
    #path('view_subject/<int:pk>/<str:grade>/<str:section>',views.view_subject,name="view_subject"),

    path('assignment_list/<int:subject>/<str:grade>/<str:section>',views.assignment_list,name="assignment_list"),
    #path('view_assignment_submission/<int:pk>',views.view_assignment_submission,name="view_assignment_submission"),
    #path('view_assignment_not_submission/<int:pk>',views.view_assignment_not_submission,name="view_assignment_not_submission"),

    #path('test_list/<int:subject>/<str:grade>/<str:section>',views.test_list,name="test_list"),
    #path('view_test_attempt/<int:pk>/<int:subject>/<str:section>',views.view_test_attempt,name="view_test_attempt"),
    #path('view_test_not_attempt/<int:pk>/<int:subject>/<str:grade>/<str:section>',views.view_test_not_attempt,name="view_test_not_attempt"),
    

    #view material
    #path('meterial_list/<int:subject>/<str:section>',views.meterial_list,name="meterial_list"),
    #path('discussion_list/<int:subject>/<str:section>',views.discussion_list,name="discussion_list"),


    #resource
    path('resource_list/',views.resource_list,name="resource_list"),
    path('video_list/<int:pk>',views.video_list,name="video_list"),
    path('add_video/<int:pk>',views.add_video,name="add_video"),
    path('video_delete/<int:pk>',views.video_delete,name="video_delete"),
    path('edit_video/<int:pk>',views.edit_video,name="edit_video"),

    path('view_class_report/<str:grade>/<str:year>',views.view_class_report,name="view_class_report"),
    path('get_subject_report/<int:subject>/<str:section>',views.get_subject_report,name="get_subject_report"),

    path('get_test_report/<int:pk>/<int:subject>/<str:grade>/<str:section>',views.get_test_report,name="get_test_report"),
    path('get_assignment_report/<int:pk>',views.get_assignment_report,name="get_assignment_report"),


    #student details
    #path('admin/user-stats',views.user_stats ,name="user_stats"),
    
    #programme add
    path('programme_list/',views.programme_list,name="programme_list"),
    path('create_chapter/<int:id>',views.create_chapter,name="create_chapter"),
    path('view_chapters/<int:id>',views.view_chapters,name="view_chapters")
   
]