from django.urls import path
from .views import QuizListView,QuizView,QuizDetail,quizsubmit, QuizAnswerDetail, my_scores, filter_scores,load_question,ajax_search_questions,ajax_load_subjects,delete_on_test
from . import views

urlpatterns = [
    path('/viewquiz',QuizListView.as_view(),name='quiz-list'),
    path('/<int:pk>',QuizDetail.as_view(),name='quiz-detail'),
    path('/quizdetail',quizsubmit),
    path('/addquiz',QuizView.as_view()),
    path('/my_scores',my_scores,name='my_scores'),
    path('/scores',filter_scores,name="scores"),
    path('/answer/<int:pk>/',QuizAnswerDetail.as_view(),name='quiz-answer-detail'),
    path('ajax_load_subjects/',ajax_load_subjects,name='ajax_load_subjects'),
    path('/delete_on_test/<int:test>/',delete_on_test,name='delete_on_test'),
    path('/load_question/',views.quiz_load_question,name='load_question'), #Test ajax load
]