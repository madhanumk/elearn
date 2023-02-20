from django.db.models import fields
from django.http import response
from resource.models import Resource, Video, Post
from rest_framework import serializers
from quiz.models import Quiz, Question, Option, Attempt, Response
from virtual_class.models import Assignment, Submission
from general.models import Student, Subject_Assignment
from quiz.models import Assignment as quizAssignment
from rest_framework.fields import CurrentUserDefault
import json
from django.http.response import JsonResponse
from django.core.serializers import serialize
from django.conf import settings




#Account
class Subject_Assignment_Serializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()

    class Meta:
        model = Subject_Assignment
        fields = ['id','subject','course_code']


#post
class Post_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','post_title']


class PostPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','post_title','post_body']
