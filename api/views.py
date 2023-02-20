from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import Post_List_Serializer, Subject_Assignment_Serializer
from resource.models import Post
from django.db.models import Q
from general.models import Subject_Assignment
# Create your views here.


class MyAuthentication(authentication.TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
            return (token.user, token)
        except:
            # modify the original exception response
            raise exceptions.AuthenticationFailed({'statusCode': 101,'message': 'Token Expired'})

        if not token.user.is_active:
            # can also modify this exception message
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (token.user, token)


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self,request):
        user = get_object_or_404(User, username=request.data.get('username'))
        user = authenticate(username=user.username, password=request.data.get('password'))
        if user:
            try:
                token = get_object_or_404(Token, user=user)
            except:
                token = Token.objects.create(user=user)

            token = token.key
            if user.groups.filter(name='Student').exists():
                user_type = "Student"
            elif user.groups.filter(name='Teacher').exists():
                user_type = "Teacher"
            elif user.groups.filter(name='School').exists():
                user_type = "School"

            return Response({'statusCode': 100,'message': 'null','token': token, 'user_type' : user_type,}, status=200)

        return Response({'statusCode': 102,'message': 'Username and password do not match'}, status=401)


class HomeView(APIView):
    authentication_classes = (MyAuthentication,)

    def get(self,request):
        user = request.user
        print(user)
        degree_category = user.student.programme.department.degree_category.category

        posts=Post.objects.filter(Q(degree_categaroy=user.student.programme.department.degree_category.id),graduation__code=user.student.programme.graduation.code,programme__department__short_name=user.student.programme.department.short_name).order_by('posted_on')            #posts = Post.objects.filter((Q(degree_categaroy=student.student.programme.department.degree_category.id)),graduation__description__in=(student.student.programme.graduation.description)).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
        subject_assignments = Subject_Assignment.objects.filter(programme=user.student.programme,year=user.student.year,semester=user.student.semester)
        
        subjects = Subject_Assignment_Serializer(subject_assignments, many=True)
        posts = Post_List_Serializer(posts, many=True)
        return Response({'statusCode': 100,'message': 'null','subjects': subjects.data,'posts':posts.data, } )