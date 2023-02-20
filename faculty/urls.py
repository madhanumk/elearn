#from django.conf.urls import url
from . import views
from django.urls import path, include


urlpatterns = [   
    
    path('faculty',views.home ,name="faculty_classroom"),
    path('view_all_assignment', views.view_all_assignment,name='view_all_assignment'),
    path('view_all_discussion', views.view_all_discussion,name='view_all_discussion'),
    path('ajax_home_assignment_filter_by_subject',views.ajax_home_assignment_filter_by_subject,name='ajax_home_assignment_filter_by_subject'),
    #path('view_assignment_not_submitted/<int:pk>', views.view_assignment_not_submitted, name='view_assignment_not_submitted'),
    path('ajax_home_discussion_filter_by_subject', views.ajax_home_discussion_filter_by_subject,name='ajax_home_discussion_filter_by_subject'),
    path('ajax_create_assignment_home',views.ajax_create_assignment_home,name="ajax_create_assignment_home"),
    path('ajax_create_session',views.ajax_create_session,name="ajax_create_session"),
    path('ajax_create_classroom',views.ajax_create_class,name="ajax_create_classroom"),
    path('ajax_discussion_filter_by_subject', views.ajax_discussion_filter_by_subject,name='ajax_discussion_filter_by_subject'),
    path('ajax_edit_session/<int:pk>',views.ajax_edit_session,name="ajax_edit_session"),
    path('ajax_delete_session/<int:pk>',views.ajax_delete_session,name="ajax_delete_session"),
    path('view_submission/<int:pk>',views.view_submission,name='view_submission'),
    path('view_assignment_not_submitted/<int:pk>', views.view_assignment_not_submitted, name='view_assignment_not_submitted'),
    path('ajax_edit_assignment/<int:pk>',views.ajax_edit_assignment,name="ajax_edit_assignment"),
    path('ajax_delete_assignment/<int:pk>',views.ajax_delete_assignment,name="ajax_delete_assignment"),
    path('ajax_edit_quiz/<int:pk>',views.ajax_edit_quiz,name="ajax_edit_quiz"),
    path('ajax_add/<str:model_name>/<int:parent_pk>',views.ajax_add_update,name="ajax_add"),
    path('ajax_topic_detail/<int:pk>',views.ajax_topic_detail,name="ajax_topic_detail"),
    path('ajax_edit/<str:model_name>/<int:pk>/<int:parent_pk>',views.ajax_add_update,name='ajax_edit'),
    path('ajax_delete/<str:model_name>/<int:pk>/<int:parent_pk>',views.ajax_delete,name='ajax_delete'),
    path('ajax_activate_quiz/<int:pk>',views.ajax_activate_quiz,name="ajax_activate_quiz"),
    path('add_test_question/<int:pk>',views.add_test_question,name="add_test_question"),
    path('import_question/<int:pk>',views.import_question,name="import_question"),
    path('question/<int:pk>/<int:quizid>', views.edit_question, name='question-update'),
    path('ajax_edit_quiz_assignment/<int:pk>',views.ajax_edit_quiz_assignment,name="ajax_edit_quiz_assignment"),
    path('ajax_delete_quiz_question/<int:pk>',views.ajax_delete_quiz_question,name="ajax_delete_quiz_question"),
    path('ajax_post_reply/<int:pk>',views.ajax_post_reply,name='ajax_post_reply'),
    path('assignment_correction/<int:pk>',views.assignment_correction,name='assignment_correction'),
    path('mark_submission/<int:pk>',views.mark_submission,name='mark_submission'),
    path('save_cfile/<int:pk>',views.save_cfile,name="save_cfile"),
        
    path('ajax_question_assign',views.ajax_question_assign,name='ajax_question_assign'),
    path('ajax_search_questions',views.ajax_search_questions,name='ajax_search_questions'),
    path('ajax_load_questions/',views.load_question,name='ajax_load_questions'),
    path('ajax_assignment_filter_by_subject',views.ajax_assignment_filter_by_subject,name='ajax_assignment_filter_by_subject'),
    path('classroom/<int:pk>', views.classroom_detail,name="classroom_detail"),
    path('chapter_detail/<int:pk>',views.chapter_detail,name="chapter_detail"),
    path('ajax_edit_classroom/<int:pk>',views.ajax_edit_class,name="ajax_edit_classroom"),
    path('ajax_delete_classroom/<int:pk>',views.ajax_delete_class,name="ajax_delete_classroom"),
    path('ajax_create_test_home',views.ajax_create_test_home,name="ajax_create_test_home"),
    path('ajax_create_test',views.ajax_create_test,name="ajax_create_test"),
    path('ajax_delete_home_quiz/<int:id>',views.ajax_delete_home_quiz,name="ajax_delete_home_quiz"),
    path('ajax_edit_assignment_detail/<int:pk>',views.ajax_edit_assignment_detail,name="ajax_edit_assignment_detail"),
    path('ajax_activate_classroom/<int:pk>',views.ajax_activate_class,name="ajax_activate_classroom"),
    path('load_section/<int:pk>/<str:model_name>',views.load_section,name='load_section'),

    
    path('ajax_get_report/', views.ajax_get_report, name='ajax_get_report'),
    path('ajax_get_assignment_report/', views.ajax_get_assignment_report, name='ajax_get_assignment_report'),
    path('view_all_test', views.view_all_test,name='view_all_test'),
    path('view_assignment_report/', views.view_assignment_report, name='view_assignment_report'),
    path('test_view_report/', views.test_view_report, name='test_view_report'),
    
    path('view_test/<int:pk>',views.view_test,name="view_test"),
    path('view_report/<int:pk>',views.view_report,name="view_report"),
    path('view_not_attempt/<int:pk>', views.view_not_attempt,name="view_not_attempt"),
    path('delete_post/<int:pk>',views.delete_post,name='delete_post'),
    path('ajax_delete_reply/<int:pk>',views.ajax_delete_reply,name='ajax_delete_reply'),
    
    #logbook
    path('log-book/',views.logbook,name="log-book"),
    path('log-book-history/<int:tab>',views.logbookhistory,name="log-book-history"),
    path('student_report/<int:pk>/<int:subject>',views.student_report,name="student_report"),
    
    #resource
    path('add_resource',views.add_resource,name="add_resource"),
    path('edit_resource/<int:id>',views.edit_resource,name="edit_resource"),
    path('delete_resource/<int:id>',views.delete_resource,name="delete_resource"),
    path('faculty_resource_list',views.faculty_resource_list,name="faculty_resource_list"),
    path('faculty_video_list/<int:id>',views.faculty_video_list,name="faculty_video_list"),
    path('faculty_add_video/<int:pk>',views.faculty_add_video,name="faculty_add_video"),
    path('faculty_edit_video/<int:pk>',views.faculty_edit_video,name="faculty_edit_video"),
    path('faculty_video_delete/<int:pk>',views.faculty_video_delete,name="faculty_video_delete"),

]