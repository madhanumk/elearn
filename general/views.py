from django.shortcuts import render
#from elearn.general.models import Programme
from .forms import CustomAuthForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as user_logout, update_session_auth_hash
from django.shortcuts import redirect
from resource.models import Resource, Post
from quiz.models import Quiz, Attempt
from django.db.models import Q
from datetime import date
from .models import Subject_Assignment,Learning_Style,Portal_Usage,Recent,Chapter
from django.db.models import Avg
import requests
import datetime
from virtual_class.models import  Submission, ClassRoom, Topic
from virtual_class.models import Assignment as vt_Assignment
from django.db.models import Sum
# Create your views here.


def test_view(request):
    return render(request, "base_2.html")

#login
class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True
    
#logout
def logout(request):
    request.session['is_logout'] = True
    user_logout(request)
    return redirect('/')

#Authorization Function
def is_student(user):
    return user.groups.filter(name='student').exists()

def is_college(user):
    return user.groups.filter(name='College').exists()

def is_faculty(user):
    return user.groups.filter(name='Faculty').exists()

def is_stud_faculty_user(user):
    return user.groups.filter(name__in=('student','Faculty','college')).exists()

@login_required(login_url='login') #Authentication
@user_passes_test(is_stud_faculty_user,login_url='login') #Authorization
def land_view(request):
    if is_student(request.user):
        user=request.user
        degree_category = user.student.programme.department.degree_category.category

        posts=Post.objects.filter(Q(degree_categaroy=user.student.programme.department.degree_category.id),graduation__code=user.student.programme.graduation.code,programme__department__short_name=user.student.programme.department.short_name).order_by('posted_on')            #posts = Post.objects.filter((Q(degree_categaroy=student.student.programme.department.degree_category.id)),graduation__description__in=(student.student.programme.graduation.description)).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
        subject_assignments = Subject_Assignment.objects.filter(programme=user.student.programme,year=user.student.year,semester=user.student.semester)
        portal_usage = Portal_Usage.objects.filter(user=request.user).aggregate(Sum('mins'))
        portal_usage = portal_usage['mins__sum']
        if portal_usage is None:
            portal_usage = 0
        return render(request, 'home.html', {'subject_assignments':subject_assignments,'posts':posts,'portal_usage':portal_usage})
        

        '''
        if degree_category == "Engineering":
            attempted = Attempt.objects.filter(user=user,Quiz__subject_assignment__programme=user.student.programme).values_list('Quiz',flat=True) 
            resources=Resource.objects.filter(subject_assignment__year=user.student.year,subject_assignment__semester=user.student.semester,subject_assignment__programme=user.student.programme)
            quizes = Quiz.objects.filter(subject_assignment__year=user.student.year,subject_assignment__semester=user.student.semester,subject_assignment__programme=user.student.programme, openDate__lte=date.today(), closeDate__gte=date.today(),isActive=True).exclude(Q(id__in=attempted)).order_by('openDate').distinct()
            assignments=vt_Assignment.objects.filter(topic__chapter__subject_assignment__programme=user.student.programme,topic__chapter__activate=True).order_by('due_date')
            posts=Post.objects.filter(Q(degree_categaroy=user.student.programme.department.degree_category.id),graduation__code=user.student.programme.graduation.code,programme__department__short_name=user.student.programme.department.short_name).order_by('posted_on')            #posts = Post.objects.filter((Q(degree_categaroy=student.student.programme.department.degree_category.id)),graduation__description__in=(student.student.programme.graduation.description)).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
            subject_assignment = Subject_Assignment.objects.filter(programme=user.student.programme,year=user.student.year,semester=user.student.semester)
            return render(request, 'home.html', {'resources':resources,'posts':posts,'quizes':quizes,'assignments':assignments,},)
        
        elif degree_category == "Arts, Science and Commerce ,Management":
            attempted = Attempt.objects.filter(user=request.user,Quiz__subject_assignment__programme=student.student.programme).values_list('Quiz',flat=True) 
            assignments=vt_Assignment.objects.filter(topic__chapter__subject_assignment__programme=student.student.programme).order_by('due_date')
            quizes = Quiz.objects.filter(subject_assignment__year=student.student.year,subject_assignment__semester=student.student.semester,subject_assignment__programme=student.student.programme, openDate__lte=date.today(), closeDate__gte=date.today(),isActive=True).exclude(Q(id__in=attempted)).order_by('openDate').distinct()
            resources=Resource.objects.filter(subject_assignment__year=student.student.year,subject_assignment__semester=student.student.semester,subject_assignment__programme=student.student.programme)
            va_resources = Resource.objects.filter(term_no__iexact='term 1',subject_assignment__programme=student.student.programme).distinct()
            posts=Post.objects.filter(Q(degree_categaroy=student.student.programme.department.degree_category.id),graduation__code=student.student.programme.graduation.code,programme__department__short_name=student.student.programme.department.short_name).order_by('posted_on')
            subject_assignment = Subject_Assignment.objects.filter(programme=student.student.programme,year=student.student.year,semester=student.student.semester)
            return render(request, 'home.html', {'resources':resources,'posts':posts,'quizes':quizes,'assignments':assignments,'va_resources':va_resources,'subject_assignment':subject_assignment},)
        
        elif degree_category == "Pharmachy":
            attempted = Attempt.objects.filter(user=request.user,Quiz__subject_assignment__programme=student.student.programme).values_list('Quiz',flat=True) 
            assignments=vt_Assignment.objects.filter(topic__chapter__subject_assignment__programme=student.student.programme,topic__chapter__activate=True).order_by('due_date')
            quizes = Quiz.objects.filter(subject_assignment__year=student.student.year,subject_assignment__semester=student.student.semester,subject_assignment__programme=student.student.programme, openDate__lte=date.today(), closeDate__gte=date.today(),isActive=True).exclude(Q(id__in=attempted)).order_by('openDate').distinct()
            resources=Resource.objects.filter(Q(subject_assignment__programme__department__degree_category__id=student.student.programme.department.degree_category.id),subject_assignment__year=student.student.year,subject_assignment__semester=student.student.semester,subject_assignment__programme=student.student.programme)
            posts=Post.objects.filter(Q(degree_categaroy=student.student.programme.department.degree_category.id),graduation__code=student.student.programme.graduation.code,programme__department__short_name=student.student.programme.department.short_name).order_by('posted_on')
            subject_assignment = Subject_Assignment.objects.filter(programme=student.student.programme,year=student.student.year,semester=student.student.semester)
            return render(request, 'home.html', {'resources':resources,'posts':posts,'quizes':quizes,'assignments':assignments,},)
        
        elif degree_category == "Architecture and Planning":
            attempted = Attempt.objects.filter(user=request.user,Quiz__subject_assignment__programme=student.student.programme).values_list('Quiz',flat=True) 
            assignments=vt_Assignment.objects.filter(topic__chapter__subject_assignment__programme=student.student.programme,topic__chapter__activate=True).order_by('due_date')
            quizes = Quiz.objects.filter(subject_assignment__year=student.student.year,subject_assignment__semester=student.student.semester,subject_assignment__programme=student.student.programme, openDate__lte=date.today(), closeDate__gte=date.today(),isActive=True).exclude(Q(id__in=attempted)).order_by('openDate').distinct()
            resources=Resource.objects.filter(Q(subject_assignment__programme__department__degree_category__id=student.student.programme.department.degree_category.id),subject_assignment__year=student.student.year,subject_assignment__semester=student.student.semester,subject_assignment__programme=student.student.programme)
            posts=Post.objects.filter(Q(degree_categaroy=student.student.programme.department.degree_category.id),graduation__code=student.student.programme.graduation.code,programme__department__short_name=student.student.programme.department.short_name).order_by('posted_on')
            subject_assignment = Subject_Assignment.objects.filter(programme=student.student.programme,year=student.student.year,semester=student.student.semester)
            return render(request, 'home.html', {'resources':resources,'posts':posts,'quizes':quizes,'assignments':assignments,},)
        '''
    elif is_faculty(request.user):
        faculty=request.user
        subject=faculty.faculty.programme
        degree_category = faculty.faculty.programme.department.degree_category.category
        
        if degree_category == "Engineering":
            posts = Post.objects.filter(programme=subject).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
            #va_resources = Resource.objects.filter(term_no__iexact='term 1',subject_assignment__programme__in=subject,subjects__subject__subject_category__category_name='Value Added').distinct().annotate(category=Max('subjects__subject__subject_category__category_name')).order_by('category','resource_name')
            va_resources = Resource.objects.filter(term_no__iexact='term 1',subject_assignment__programme=subject)
            quizes = Quiz.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            resources=Resource.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            return render(request, 'home.html', {'resources':resources,'quizes':quizes,'va_resources':va_resources,'posts':posts},)
        
        elif degree_category == "Arts, Science and Commerce ,Management":
            posts = Post.objects.filter(programme=subject).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
            va_resources = Resource.objects.filter(term_no__iexact='term 1',subject_assignment__programme=subject)
            quizes = Quiz.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            resources=Resource.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            return render(request, 'home.html', {'resources':resources,'quizes':quizes,'va_resources':va_resources,'posts':posts},)
        
        elif degree_category == "Pharmachy":
            posts = Post.objects.filter(programme=subject).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
            va_resources = Resource.objects.filter(term_no__iexact='term 1',subject_assignment__programme__in=subject)
            quizes = Quiz.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            resources=Resource.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            return render(request, 'home.html', {'resources':resources,'quizes':quizes,'va_resources':va_resources,'posts':posts},)
        
        elif degree_category == "Architecture and Planning":
            posts = Post.objects.filter(programme=subject).order_by('posted_on').exclude(expires_on__lt=date.today()).distinct()
            va_resources = Resource.objects.filter(term_no__iexact='term 1',subject_assignment__programme__in=subject)
            quizes = Quiz.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            resources=Resource.objects.filter(subject_assignment__programme = faculty.faculty.programme)
            return render(request, 'home.html', {'resources':resources,'quizes':quizes,'va_resources':va_resources,'posts':posts},)
        
    elif request.user.groups.filter(name='College').exists():
        return redirect('/college_admin')
    
    '''
    elif is_college(request.user):
        college=request.user
        category=college.college.category
        #degree_category = faculty.faculty.programme.department.degree_category.category
        resources=Resource.objects.filter(subject_assignment__programme__department__degree_category = category)
        return render(request, 'home.html', {'resources':resources})
        '''

@login_required
def chapter_list(request,id):
    user = request.user
    subject_assignment = Subject_Assignment.objects.get(id=id)
    chapters = Chapter.objects.filter(subject_assignment__id=id)
    resources=Resource.objects.filter(subject_assignment=subject_assignment)
    attempt = list(Attempt.objects.filter(user=request.user).values_list('Quiz__id', flat=True))   
    quizes = Quiz.objects.filter(subject_assignment=subject_assignment, openDate__lte=date.today(),closeDate__gte=date.today(),isActive=True).exclude(id__in=attempt)
    subject_assignments = Subject_Assignment.objects.filter(programme=user.student.programme,year=user.student.year,semester=user.student.semester)
    return render(request,'vt_class/chapter_details.html',{'chapters':chapters,'subject_assignment':subject_assignment,'resources':resources,'quizes':quizes,'subject_assignments':subject_assignments,})



@login_required
def edit_profile(request):
    if is_student(request.user):
        learning_styles = Learning_Style.objects.filter(student=request.user.student)
        quiz_id = None

        if not learning_styles:
            #quiz = Quiz.objects.get(name="VAK Learning Style")
            quiz = Quiz.objects.get(name="quiz-1")
            quiz_id =  quiz.id

        #return render(request, 'edit_profile.html', {'learning_styles':learning_styles,'quiz_id':quiz_id})
        return render(request, 'accounts/edit_profile.html', )
    else:
        return render(request, 'accounts/edit_profile.html', )
    
@login_required
def dashboard(request):    
    if is_student(request.user):
        subjects = Subject_Assignment.objects.filter(programme =request.user.student.programme)
        learning_styles = Learning_Style.objects.filter(student=request.user.student)
        school_usage = Portal_Usage.objects.filter(user__student__programme=request.user.student.programme).aggregate(Avg('mins'))
        your_usage = Portal_Usage.objects.filter(user=request.user).aggregate(Avg('mins'))
        #attempts = Attempt.objects.filter(user=request.user).order_by('-date').values_list('Quiz__id',flat=True).distinct()
        attempts = Attempt.objects.filter(user=request.user).order_by('-date')
        needs_to_improve_resources  = []
        more_concentrate_on_resources  = []
        performing_resources  = []
        for subject in subjects:
            score = Attempt.objects.filter(user=request.user).aggregate(Avg('score'))
            try:
                attempt = int(score['score__avg'])
                stud = request.user.student
                if stud.board.board == "State Board":
                    resources = Resource.objects.filter((Q(school=stud.school) | Q(school__isnull=True)),term_no__iexact='term 1',language_medium__language__in=(stud.medium.language,'Common'),subjects__group=stud.group,subjects__grade=stud.grade,subjects__board=stud.board,subjects=subject).distinct()
                else:
                    resources = Resource.objects.filter((Q(school=stud.school) | Q(school__isnull=True)),term_no__iexact='term 1',subjects=subject).exclude(subjects__subject__subject_category__category_name='Value Added').distinct()
                if attempt < 50:      
                    for resource  in resources:
                        more_concentrate_on_resources.append(resource)
                elif attempt < 71:
                    for resource  in resources:
                        needs_to_improve_resources.append(resource)                    
                else:
                    for resource  in resources:
                        performing_resources.append(resource)
            except:
                pass

        stud = request.user.student
        submissions = Submission.objects.filter(student=stud)
        crooms=ClassRoom.objects.filter(subject_assignment__programme=stud.programme,activate=True)       
        chapters = Chapter.objects.filter(subject_assignment__programme=stud.programme)
        needs_to_improve_croom = []
        more_concentrate_on_croom = []
        performing_croom = []
        for chapter in chapters:

            mark = Submission.objects.filter(student=request.user.student,assignment__topic__chapter__in=(chapter,)).aggregate(Avg('marks'))
            try:
                mark = int(mark['marks__avg'])

                if mark < 50:
                    more_concentrate_on_croom.append(chapter)
                elif mark < 71:
                    needs_to_improve_croom.append(chapter)
                    
                else:
                    performing_croom.append(chapter)
            except:
                pass


        topic = Topic.objects.filter(chapter__in=chapters).order_by('created_on')

        submitted_assignments = Submission.objects.filter(student=stud).values_list('assignment',flat=True)
 
        assignments= vt_Assignment.objects.filter(topic__in=topic,topic__chapter__subject_assignment__year=stud.year,topic__chapter__subject_assignment__semester=stud.semester).exclude(id__in=submitted_assignments).order_by('due_date')
        
        croom=ClassRoom.objects.filter(subject_assignment__programme=stud.programme,activate=True)       
        if stud.programme.department.degree_category.category == request.user.student.programme.department.degree_category:
            quizes = Quiz.objects.filter(subject_assignment__programme=stud.programme,subject_assignment__year=stud.year,subject_assignment__semester=stud.semester, openDate__lte=date.today(), closeDate__gte=date.today(),isActive=True).exclude(Q(id__in=attempts) ).order_by('openDate').distinct()
        else:
            quizes = Quiz.objects.filter(subject_assignment__programme=stud.programme,subject_assignment__year=stud.year,subject_assignment__semester=stud.semester, openDate__lte=date.today(), closeDate__gte=date.today(),isActive=True).exclude(Q(id__in=attempts)).order_by('openDate').distinct()

        url = "http://learn-buddy.in/trait-api/"+request.user.student.mobile_no

    elif is_faculty(request.user):
        subjects = request.user.faculty.programme.title
        learning_styles = None
        school_usage = Portal_Usage.objects.filter(user__student__programme=request.user.faculty.programme).aggregate(Avg('mins'))
        your_usage = Portal_Usage.objects.filter(user=request.user).aggregate(Avg('mins')) 
        attempts = Attempt.objects.filter(user=request.user,Quiz__subject_assignment__programme__title__in=subjects).order_by('-date') 
        quizes = None
        submissions= None
        assignments = None
        more_concentrate_on_resources = None
        needs_to_improve_resources = None
        performing_resources = None
        needs_to_improve_croom= None
        more_concentrate_on_croom= None
        performing_croom = None
        url = "http://learn-buddy.in/trait-api/"+request.user.faculty.mobile_no
    
    histories = Recent.objects.filter(user=request.user).order_by('-date')
  
    '''
    response = requests.get(url,headers={'User-Agent': 'Chrome'})
    data = response.json()
    if data['attempted'] == True:
        personality = data['trait']['personality']
        personality_test_attempted = True
    else:
        personality = None
        personality_test_attempted = False
    '''
    general_usage = Portal_Usage.objects.filter(user__student__isnull=False).aggregate(Avg('mins'))
    print(general_usage['mins__avg'])
    #general_usage = int(general_usage['mins__avg'])
    general_usage = int(300)

    #school_usage = int(school_usage['mins__avg'])
    school_usage = int(300)
    #your_usage = int(your_usage['mins__avg'])
    your_usage = int(300)
   
    return render(request, 'accounts/dashboard.html', {'performing_croom':performing_croom,'more_concentrate_on_croom':more_concentrate_on_croom,'needs_to_improve_croom':needs_to_improve_croom,'performing_resources':performing_resources,'needs_to_improve_resources':needs_to_improve_resources,'more_concentrate_on_resources':more_concentrate_on_resources,'assignments':assignments,'submissions':submissions,'quizes':quizes,'your_usage':your_usage ,'general_usage':general_usage,'school_usage':school_usage,'learning_styles':learning_styles,'attempts':attempts,'histories': histories,'personality':'personality','personality_test_attempted':'personality_test_attempted'})

@login_required
def draw_usage(request):
    data = dict()
    day_count = int(request.GET.get('days'))
    labels = []
    mins = []

    delta = datetime. timedelta(days=day_count)
    end_date = datetime.datetime.today() + datetime.timedelta(days = 1)
    start_date = end_date - delta
    s_date = start_date

    delta = datetime. timedelta(days=1)
    while start_date <= end_date:
        labels.append(start_date.date())
        start_date += delta

    queryset = Portal_Usage.objects.filter(user=request.user,date__gte=s_date).values_list('date','mins')
    
    for date in labels:
        for entry in queryset:
            if date == entry[0]:
                mins.append(entry[1])
                break
        else:
            mins.append(0)
    data['date'] = labels
    data['mins'] = mins
    return JsonResponse(data) 


@login_required
def draw_chart(request):
    data = dict()
    if is_student(request.user):
        stud = request.user.student
        subjects = list(Subject_Assignment.objects.filter(programme=stud.programme,year=stud.year,semester=stud.semester).values_list('id','subject__subject_title').order_by('subject__subject_title'))
    elif is_faculty(request.user):
        stud = request.user.faculty
        subjects =list(Subject_Assignment.objects.filter(programme=request.user.faculty.programme,year=stud.year,semester=stud.semester).values_list('id','subject__subject_title'))

    sub_title = list()
    sub_assign = list()
    scores = list()
    for sub in subjects:
        if is_faculty(request.user):
            sub_title.append(sub[1]+"-"+sub[2])
        else:
            sub_title.append(sub[1])
        sub_assign.append(sub[0])
    data['subjects'] = sub_title
    for sub in sub_assign:
        scores.append(list(Attempt.objects.filter(user=request.user,Quiz__subject_assignment__in=(sub,)).values_list('score',flat=True)))
    data['scores'] = scores

    labels = []
    mins = []

    delta = datetime. timedelta(days=7)
    end_date = datetime.datetime.today() + datetime.timedelta(days = 1)
    start_date = end_date - delta
    s_date = start_date

    delta = datetime. timedelta(days=1)
    while start_date <= end_date:
        labels.append(start_date.date())
        start_date += delta

    queryset = Portal_Usage.objects.filter(user=request.user,date__gte=s_date).values_list('date','mins')
    
    for date in labels:
        for entry in queryset:
            if date == entry[0]:
                mins.append(entry[1])
                break
        else:
            mins.append(0)
    data['date'] = labels
    data['mins'] = mins

    return JsonResponse(data) 

@login_required
def my_personality(request):

    domain = "http://learn-buddy.in/trait-api/"

    if is_student(request.user):
        mobile_no = request.user.student.mobile_no
    elif is_faculty(request.user):
        mobile_no = request.user.faculty.mobile_no


    url = domain+mobile_no
    response = requests.get(url,headers={'User-Agent': 'Chrome'})
    data = response.json()
    if data['attempted'] == True:
        personality = data['trait']['personality']
        traits = []
        for i in range(4):
            traits.append(data['trait']['trait'+str(i+1)])

        jobs = []
        for i in range(5):
            job_name = data['jobs'][i]['job']
            jobs.append(job_name)
        attempted = True

    else:
        attempted = False
        jobs= None
        traits = None
        personality  = None
    return render(request, 'my_personality.html', {'personality':personality,'attempted': attempted,'jobs':jobs,'traits':traits})