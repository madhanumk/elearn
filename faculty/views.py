from re import sub
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from general.views import is_student, is_stud_faculty_user, is_faculty
from virtual_class.models import ClassRoom,Assignment,Forum,Upcoming_Session,Reply
from quiz.models import Quiz,Attempt
from virtual_class.models import ClassRoom,Topic,Material,Video,Submission
from virtual_class.forms import ReplyForm
from datetime import datetime, date
from general.models import Faculty_Subject_Assignment,Subject_Assignment,Student,Subject,Programme,Chapter
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .forms import ClassRoomForm,AssignmentForm,Upcoming_SessionForm,QuizForm,Log_Book_Form,Log_Book_Entry_FormSet,Log_Book_Entry,SubmissionForm,TopicForm,VideoForm,MaterialForm,QuestionForm,OptionFormSet,NewOptionFormSet,QuizAssignmentForm
from .models import Log_Book
from quiz import models as qm
from resource.models import Resource,Video as Re_Video
from resource.forms import ResourceForm
from college.forms import VideoForm as Re_VideoForm
import openpyxl
# Create your views here.
#Landing Page Views with Authentication and Authorization
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def home(request):
    user = request.user
    faculty_subject_assignment = Faculty_Subject_Assignment.objects.filter(faculty__user=user).values_list('subject',flat=True).distinct()   
    classrooms = ClassRoom.objects.filter(created_by=user).order_by('activate')
    assignments = Assignment.objects.filter(topic__chapter__subject_assignment__in=faculty_subject_assignment).order_by('-posted_on')[:6]
    discussions = Forum.objects.filter(topic__chapter__subject_assignment__in=faculty_subject_assignment).order_by('-created_on')[:6]
    sessions = Upcoming_Session.objects.filter(classroom__created_by=request.user,start_date__gte=datetime.now()).order_by('start_date','start_time')
    subjects= user.faculty.programme
    subject_assignments=Subject_Assignment.objects.filter(programme=subjects)
    quiz=Quiz.objects.filter(subject_assignment__programme=request.user.faculty.programme).order_by('-openDate').distinct()[:6]

    form = ReplyForm()
    context ={
        'classrooms':classrooms,
        'assignments':assignments,
        'discussions':discussions,
        'sessions':sessions,
        'form' : form,
        'quizes' : quiz,
        'subject_assignments':subject_assignments,
    }
    return render(request,'admin/custom/home.html',context)


@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_all_assignment(request):
    user = request.user
    subject_assignment= Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty).distinct().values_list('subject',flat=True)
    print("subject_assignment",subject_assignment)
    subject_assignments = Subject_Assignment.objects.filter(id__in=subject_assignment)

    assignments = Assignment.objects.filter(topic__chapter__subject_assignment__in=subject_assignment).order_by('-posted_on')

    context ={
        'subject_assignments':subject_assignments,
        'assignments':assignments
    }
    return render(request,'admin/custom/assignments.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_all_test(request):   
    #subjects= Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty).distinct().values_list('subject',flat=True)
    subjects= Faculty_Subject_Assignment.objects.filter(faculty__user__id=request.user.id)
    quizzes=Quiz.objects.filter(subject_assignment__subjects__in=subjects).order_by('-openDate').distinct()
    print("quizes",quizzes)
    context ={       
        'quizzes':quizzes,
    }
    return render(request,'admin/custom/quiz/view_all_quiz.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_all_discussion(request):
    user = request.user.faculty
    faculty_subject_assignment = Faculty_Subject_Assignment.objects.filter(faculty=user).values_list('subject',flat=True)
    print(faculty_subject_assignment)
    discussions = Forum.objects.filter(topic__chapter__subject_assignment__in=faculty_subject_assignment).order_by('-created_on')
    subjects=request.user.faculty.programme.title
    subject= user.programme
    subject_assignments=Subject_Assignment.objects.filter(programme=subject)        
    form = ReplyForm()
    context ={
       
        'discussions':discussions,
        'form' : form,
        'subjects':subjects,
        'subject_assignments':subject_assignments
    }
    return render(request,'admin/custom/discussions.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def classroom_detail(request,pk):
    user = request.user
    chapter = Chapter.objects.get(id=pk)
    classroom_id = ClassRoom.objects.filter(subject_assignment=chapter.subject_assignment).values_list('id',flat=True).distinct()
    for classroom in classroom_id:
        classroom_id = classroom
        print("classroom",classroom_id)
    if chapter:
        #chapter = Chapter.objects.filter(subject_assignment=classroom.subject_assignment)
        print("chapter-test",chapter)
        topics = Topic.objects.filter(chapter=chapter).order_by('id')
        materials = Material.objects.filter(topic__chapter=chapter).order_by('-added_on')[:6]
        videos = Video.objects.filter(topic__chapter=chapter).order_by('-added_on')[:6]
        context={
            'chapter':chapter,
            'classroom':classroom_id,
            'topics':topics,
            'materials':materials,
            'videos':videos
        }
        return render(request,'admin/custom/classroom_detail.html',context)
    else:
        return HttpResponse('Access Denied')
    

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def chapter_detail(request,pk):
    user = request.user
    classroom = ClassRoom.objects.get(id=pk)
    if classroom.created_by == user:
        chapter = Chapter.objects.filter(subject_assignment=classroom.subject_assignment)
        print("chapter-test",chapter)
        context={
            'chapter':chapter,
            'classroom':classroom,
        }
        return render(request,'admin/custom/subject_detail.html',context)
    else:
        return HttpResponse('Access Denied')
    
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_edit_class(request,pk):
    user = request.user
    data = dict()
    classroom = ClassRoom.objects.get(id=pk)
    if request.method == 'POST':
        form = ClassRoomForm(request.POST,request=request,instance=classroom)
        if form.is_valid() and classroom.created_by == user:
            classroom = form.save()
            classrooms = ClassRoom.objects.filter(created_by=user).order_by('activate')
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/classrooms.html',{'classrooms':classrooms},request)
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/classform.html',{'form':form,'operation':'Update','classroom_id':classroom.id},request)
        
    else:
        form = ClassRoomForm(request=request,instance=classroom)
        print(form)
        data['form'] = render_to_string('admin/custom/classform.html',{'form':form,'operation':'Update','classroom_id':classroom.id},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_delete_class(request,pk):
    user = request.user
    data = dict()
    classroom = ClassRoom.objects.get(id=pk)
    if classroom.created_by == user:
        classroom.delete()
        classrooms = ClassRoom.objects.filter(created_by=user).order_by('activate')
        data['valid'] = True
        data['html'] = render_to_string('admin/custom/classrooms.html',{'classrooms':classrooms},request)
    else:
        data['valid'] = False
        
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_assignment_report(request):
    degree_category=request.user.faculty.programme.department.degree_category
    department = request.user.faculty.department
    #subjects= Subject.objects.filter(degree_categaroy= degree_category,subject_category=request.user.faculty.subject_category)
    subjects= Subject_Assignment.objects.filter(programme=request.user.faculty.programme)
    #section=section_options
    print(subjects)

    context={
        'subjects':subjects,
        #'section': section, 
    }

    return render(request,'admin/custom/assignment_report_download.html',context)

#Download Test Report
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def test_view_report(request):
    subjects= Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty).distinct().values_list('subject',flat=True)
    subjects = Subject_Assignment.objects.filter(id__in=subjects)
    #section=section_options

    context={
        'subjects':subjects,
        #'section': section, 
    }

    return render(request,'admin/custom/quiz/report_download.html',context)


@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_home_assignment_filter_by_subject(request):
    data=dict()
    user = request.user
    subject_assignment = request.POST.get('subject')

    if subject_assignment == "all":
        assignments = Assignment.objects.filter(topic__chapter__subject_assignment=subject_assignment).order_by('-posted_on')[:6]
    else:
        assignments = Assignment.objects.filter(topic__chapter__subject_assignment=subject_assignment).order_by('-posted_on')[:6]

    context ={       
        'assignments':assignments
    }

    data['html'] = render_to_string('admin/custom/assignments_filter_by_subject_home.html',context,request)
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_home_discussion_filter_by_subject(request):

    data=dict()
    user = request.user
    if request.POST.get('subject') == "all":
        discussions = Forum.objects.filter(topic__chapter__created_by=user).order_by('-created_on')[:6]
    else:
         discussions = Forum.objects.filter(topic__chapter__subject_assignment=request.POST.get('subject')).order_by('-created_on')[:6]  
    form = ReplyForm()
    context ={
       
        'discussions':discussions,
        'form' : form,
    }

    data['html'] = render_to_string('admin/custom/discussions_filter_by_subject.html',context,request)
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_create_assignment_home(request):
    data = dict()
    if request.method == 'POST':
        form = AssignmentForm(request.POST,request.FILES,request=request)
        if form.is_valid():
            form.save()
            assignments = Assignment.objects.filter(topic__faculty_subject_assignment__faculty__user=request.user).order_by('-posted_on')[:6]
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/assignment.html',{'assignments':assignments},request)
            return JsonResponse(data)
        else:
            data['valid'] = False
                    
    else:
        form = AssignmentForm(request=request)

    context = {
        'form':form,
        'operation':'Add'       
        }
                
    data['form'] = render_to_string('admin/custom/assignmentform.html',context,request)
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_create_session(request):
    data = dict()
    if request.method == 'POST':
        form = Upcoming_SessionForm(request.POST,request=request)
        if form.is_valid():
            session = form.save()
            sessions = Upcoming_Session.objects.filter(classroom__created_by=request.user,start_date__gte=datetime.now()).order_by('start_date','start_time')
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/session.html',{'sessions':sessions},request)
            return JsonResponse(data)
        else:
            data['valid'] = False
                    
    else:
        form = Upcoming_SessionForm(request=request)

    context = {
        'form':form,
        'operation':'Add'       
        }
                
    data['form'] = render_to_string('admin/custom/sessionform.html',context,request)
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_create_class(request):
    user = request.user
    data = dict()
    if request.method == 'POST':
        form = ClassRoomForm(request.POST,request=request)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.created_by = user
            #classroom.school = user.teacher.school
            classroom.save()
            classrooms = ClassRoom.objects.filter(created_by=user).order_by('activate')
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/classrooms.html',{'classrooms':classrooms},request)
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/classform.html',{'form':form,'operation':'Add'},request)
        
    else:
        form = ClassRoomForm(request=request)
        data['form'] = render_to_string('admin/custom/classform.html',{'form':form,'operation':'Add'},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_create_test_home(request):
    user = request.user
   
    data = dict()
    if request.method == 'POST':
        form = QuizForm(request.POST,request=request)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = user
            #quiz.school = user.teacher.school
            quiz.isActive= False
            duration=request.POST.get('duration_in_minutes')
            #quiz.language_medium=user.teacher.medium
            if int(duration) > 0:
                quiz.timed_exam = True
            else:
                quiz.timed_exam = False

            quiz.save()
            form.save_m2m()
           

            quizes=Quiz.objects.filter(created_by=request.user).distinct().order_by('-openDate')[:6]
            data['valid'] = True
           
            data['html'] = render_to_string('admin/custom/quiz/quiz.html',{'quizes':quizes},request)
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/quiz/quizform.html',{'form':form,'operation':'Add'},request)
        
    else:
        form = QuizForm(request=request)
        data['form'] = render_to_string('admin/custom/quiz/quizform.html',{'form':form,'operation':'Add'},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_assignment_filter_by_subject(request):
    data=dict()
    user = request.user   
    subject_assignment = request.POST.get('subject')

    if subject_assignment == "all":
        assignments = Assignment.objects.filter(topic__croom__created_by=user).order_by('-posted_on')

    else:
        #assignments = Assignment.objects.filter(topic__croom__created_by=user,topic__croom__subject=subject_assignment).order_by('-posted_on')
        assignments = Assignment.objects.filter(topic__croom__created_by=user).order_by('-posted_on')

    context ={
       
        'assignments':assignments
    }

    data['html'] = render_to_string('admin/custom/assignments_filter_by_subject.html',context,request)
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_create_test(request):
    user = request.user

    data = dict()
    if request.method == 'POST':
        form = QuizForm(request.POST,request=request)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = user
            #quiz.school = user.teacher.school
            quiz.isActive= False
            duration=request.POST.get('duration_in_minutes')
            #quiz.language_medium=user.teacher.medium
            if int(duration) > 0:
                quiz.timed_exam = True
            else:
                quiz.timed_exam = False

            quiz.save()
            form.save_m2m()         

           
            data['valid'] = True
           
            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/quiz/quiz_form_details_page.html',{'form':form,'operation':'Add'},request)
        
    else:
        form = QuizForm(request=request)
        data['form'] = render_to_string('admin/custom/quiz/quiz_form_details_page.html',{'form':form,'operation':'Add'},request)
    
    return JsonResponse(data)


@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_discussion_filter_by_subject(request):
    data=dict()
    user = request.user 
    if request.POST.get('subject') == "all":
        discussions = Forum.objects.filter(topic__croom__created_by=user).order_by('-created_on')
    else:
        discussions = Forum.objects.filter(topic__chapter__subject_assignment=request.POST.get('subject')).order_by('-created_on')
    #subjects=request.user.faculty.programme.all()
        
    form = ReplyForm()
    context ={
       
        'discussions':discussions,
        'form' : form,
        #'subjects':subjects,
    }

    data['html'] = render_to_string('admin/custom/discussions_filter_by_subject.html',context,request)
    return JsonResponse(data)
   
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_get_assignment_report(request):
    subject_assignment= request.POST.get('subject')
    #section= request.POST.get('section')
    subject_assignment=Subject_Assignment.objects.get(id=subject_assignment)
    students= Student.objects.filter(programme=subject_assignment.programme)
    assignments=Assignment.objects.filter(topic__chapter__subject_assignment=subject_assignment)
  
    student_name=list()
    student_username=list()
    assignment_name=list()
    score=list()
    status= list()    

    for assignment in assignments:
            assignment_name.append(assignment.title)

    for student in students:
        student_name.append(student.user.get_full_name())
        student_username.append(student.user.username)
        
        assignment_count=0
        attended= 0

        for assignment in assignments:
            assignment_count+=1            

            try:
                submission=Submission.objects.get(student=student,assignment=assignment,status="A")
                score.append(submission.marks)
                attended+=1
            except:
                score.append("Not Submitted")        

        status.append(str(attended) + '/' + str(assignment_count))


    data=dict()    
    data['student_name'] = student_name
    data['student_username']= student_username
    data['assignment_name']=assignment_name
    data['score']=score
    data['status']=status

    return JsonResponse(data)  

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_get_report(request):
    subject= request.POST.get('subject')
    #section= request.POST.get('section')
    subject_assignment=Subject_Assignment.objects.get(id=subject)
    print(subject_assignment)
    students= Student.objects.filter(programme=subject_assignment.programme)
    all_quiz= qm.Quiz.objects.filter(subject_assignment=subject_assignment).distinct()


    student_name=list()
    student_username=list()
    test_name=list()
    score=list()
    status= list()
    

    for quiz in all_quiz:

            test_name.append(quiz.name)

    for student in students:
        student_name.append(student.user.get_full_name())
        student_username.append(student.user.username)
        
        quiz_count=0
        attended= 0

        for quiz in all_quiz:
            quiz_count+=1            

            try:
                attempt=Attempt.objects.get(user=student.user,Quiz=quiz)
                score.append(attempt.score)
                attended+=1
            except:
                score.append("Not Attended")


        status.append(str(attended) + '/' + str(quiz_count))



    data=dict()

    data['student_name'] = student_name
    data['student_username']= student_username

    data['test_name']=test_name
    data['score']=score
    data['status']=status

    return JsonResponse(data) 

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_edit_session(request,pk):
    user = request.user
    data = dict()
    session = Upcoming_Session.objects.get(id=pk)
    if request.method == 'POST':
        form = Upcoming_SessionForm(request.POST,request=request,instance=session)
        if form.is_valid() and session.classroom.created_by == user:
            form.save()
            
            data['valid'] = True
            sessions = Upcoming_Session.objects.filter(classroom__created_by=request.user,start_date__gte=datetime.now()).order_by('start_date','start_time')
            data['html'] = render_to_string('admin/custom/session.html',{'sessions':sessions},request)
            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/sessionform.html',{'form':form,'operation':'Update','session_id':pk},request)
        
    else:
        form = Upcoming_SessionForm(request=request,instance=session)
        data['form'] = render_to_string('admin/custom/sessionform.html',{'form':form,'operation':'Update','session_id':pk},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_delete_session(request,pk):
    user = request.user
    data = dict()
    session = Upcoming_Session.objects.get(id=pk)
    if session.classroom.created_by == user:
        session.delete()
        data['valid'] = True
        sessions = Upcoming_Session.objects.filter(classroom__created_by=request.user,start_date__gte=datetime.now()).order_by('start_date','start_time')
        data['html'] = render_to_string('admin/custom/session.html',{'sessions':sessions},request)
    else:
        data['valid'] = False
        
    return JsonResponse(data)

#logbook entry

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def logbook(request): 

    subjects = Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty)
    print(subjects)
    tab = request.GET.get('tab')
    if tab:
        tab = int(tab)
    else:
        tab = 1 

    counter = 1
    for  subject in subjects:
        if counter == tab:
            subject_instance = subject
        counter += 1
    
    if request.method == "POST":
        data = dict()
        try:
            log_book = Log_Book.objects.get(subject=subject_instance,date=date.today())            
            logbookform = Log_Book_Form(request.POST, instance=log_book,request=request)
            logbookentryform = Log_Book_Entry_FormSet(request.POST,instance=log_book)
        except:
            logbookform = Log_Book_Form(request.POST,request=request)
            parent_logbook = logbookform.save(commit=False)
            logbookentryform = Log_Book_Entry_FormSet(request.POST,instance=parent_logbook)
            
        if logbookform.is_valid() and logbookentryform.is_valid():
            parent_logbookform = logbookform.save(commit=False)    
            parent_logbookform.subject = subject_instance
            parent_logbookform.save()                           
            logbookentryform.save()
            data['valid'] = True
            
            return JsonResponse(data)
        else:
            data['valid'] = False
            return JsonResponse(data)
            
    else:    
        try:
            log_book = Log_Book.objects.get(subject=subject_instance,date=date.today())
            if log_book.is_day_update:
                context = {
                 'subjects': subjects,      
                 'tab':tab,
                 'log_book':log_book,
                }
                return render(request,'faculty/logbook/day_updated_logbook.html',context)

            logbookform = Log_Book_Form(request=request,instance=log_book)
            logbookentryform = Log_Book_Entry_FormSet(instance=log_book)
        except:
            logbookform = Log_Book_Form(request=request,)
            logbookentryform = Log_Book_Entry_FormSet()
            log_book = None

 
        context = {
          'subjects': subjects,
          'logbookform':logbookform,
          'logbookentryform':logbookentryform,
          'tab':tab,
          'log_book':log_book,
        }
        return render(request,'faculty/logbook/logbook.html',context)
    
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def logbookhistory(request,tab):
    teacher_subjects = Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty)
    counter = 1
    for  subject in teacher_subjects:
        if counter == tab:
            subject_instance = subject
        counter += 1
    
    log_book_entries = Log_Book_Entry.objects.filter(log_book__subject=subject_instance)
    context = {
      'log_book_entries':log_book_entries, 
      'tab': tab, 
      'subjects': teacher_subjects,
      'subject_instance':subject_instance,
    }
    return  render(request,'faculty/logbook/logbook-history.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def student_report(request,pk,subject):
    print(pk)
    print(subject)
    data = dict()
    student = Student.objects.get(id=pk,programme__department__degree_category=request.user.faculty.category)
    subject = Subject_Assignment.objects.get(id=subject)
    assignments = Assignment.objects.filter(topic__croom__subject_assignment=subject)
    assignment_name = []
    assignment_mark = []
    submission_status = []
    assignment_due_date = []
    for assignment in assignments:
        assignment_name.append(assignment.title)
        assignment_due_date.append(assignment.due_date)
        try:
            submission = Submission.objects.get(student=student,assignment=assignment)               
            submission_status.append(submission.get_status_display())  
            assignment_mark.append(submission.marks)
        except:
            submission_status.append('Not Submitted')
            assignment_mark.append(0)


    tests = Quiz.objects.filter(subject_assignment=subject,subject_assignment__programme__department__degree_category=request.user.faculty.category).distinct()
    test_name = []
    test_mark = []
    attempt_status = []
    test_due_date = []

    for test in tests:
        test_due_date.append(test.closeDate)
        test_name.append(test.name)
        try:
            attempt = Attempt.objects.get(user=student.user,Quiz=test)               
            attempt_status.append('Attempted')  
            test_mark.append(attempt.score)
        except:
            attempt_status.append('Not Attempted')
            test_mark.append(0)

    assignments =  []
    assignments = zip(assignment_name,submission_status,assignment_mark,assignment_due_date)
    tests =  []
    tests = zip(test_name,attempt_status,test_mark,test_due_date)
    data['assignment_name'] = assignment_name
    data['assignment_mark'] = assignment_mark
    data['submission_status'] = submission_status
    data['test_name'] = test_name
    data['test_mark'] = test_mark
    data['attempt_status'] = attempt_status
    data['student_name'] = str(student)
    data['assignments'] = render_to_string('admin/custom/student_assignment_report.html',{'assignments':assignments,},request)
    data['tests'] = render_to_string('admin/custom/student_test_report.html',{'tests':tests,},request)

    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_submission(request,pk):
    assignment = Assignment.objects.get(id=pk)
    if assignment.topic.faculty_subject_assignment.faculty.user == request.user:
        form = SubmissionForm()
        return render(request,'admin/custom/submission.html',{'assignment':assignment})
    return HttpResponse('Access Denied')


@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_assignment_not_submitted(request,pk):
    assignment=Assignment.objects.get(id=pk)
    submittedd_list=Submission.objects.filter(assignment_id=pk).values_list('student')   
    subject_assignment=Subject_Assignment.objects.get(id=assignment.topic.croom.subject_assignment.id)
    students = Student.objects.filter(programme__department__degree_category=request.user.faculty.category,programme=subject_assignment.programme).exclude(id__in=submittedd_list)
    
    context={
        'students':students,
        'assignment':assignment,
    }
    return render(request,'admin/custom/view_not_submitetd.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_edit_assignment(request,pk):
    user = request.user
    data = dict()
    assignment = Assignment.objects.get(id=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST,request.FILES,request=request,instance=assignment)
        if form.is_valid() and assignment.topic.croom.created_by == user:
            form.save()
            assignments = Assignment.objects.filter(topic__croom__created_by=request.user).order_by('-posted_on')[:6]
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/assignment.html',{'assignments':assignments},request)
            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/assignmentform.html',{'form':form,'operation':'Update','assignment_id':pk},request)
        
    else:
        form = AssignmentForm(request=request,instance=assignment)
        data['form'] = render_to_string('admin/custom/assignmentform.html',{'form':form,'operation':'Update','assignment_id':pk},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_delete_assignment(request,pk):
    print(pk)
    user = request.user
    data = dict()
    assignment = Assignment.objects.get(id=pk)
    if assignment.topic.croom.created_by == user:
        assignment.delete()
        assignments = Assignment.objects.filter(topic__croom__created_by=request.user).order_by('-posted_on')[:6]
        data['valid'] = True
        data['html'] = render_to_string('admin/custom/assignment.html',{'assignments':assignments},request)
    else:
        data['valid'] = False
        
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_test(request,pk):
    quiz=Quiz.objects.get(id=pk)
    programe = []
    subject = []
    teacher_subjects =  Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty)
    for teacher_subject in teacher_subjects:
        programe.append(teacher_subject)
        subject.append(teacher_subject.subject.subject.id)
    subjects = Subject.objects.filter(id__in=subject).distinct()
    grades =  Programme.objects.filter(id=request.user.faculty.programme.id).distinct()
    subject_assignment = Subject_Assignment.objects.filter(programme__id__in=grades)
    print(subject_assignment)
    context ={
       
        'quiz':quiz,
        'grades':grades,
        'subjects' : subjects,
        'object_id':quiz.id,
        'subject_assignment':subject_assignment,
    }
    return render(request,'admin/custom/quiz/view_test.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_report(request,pk):
    subjects = Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty).distinct().values_list('subject', flat=True)
    try:
        quiz=Quiz.objects.get(id=pk,subject_assignment__programme=request.user.faculty.programme,subject_assignment__in=subjects)
    except:
        return JsonResponse("Access Denied..!")
    attempts=Attempt.objects.filter(Quiz=quiz).exclude(user__groups__name="teacher")
    #grade=Subject_Assignment.objects.filter(id__in=subjects).values('grade')   
    #grades=Grade.objects.filter(id__in=grade)

    context ={
       
        'quiz':quiz,
        'attempts': attempts,
        'grades' :"grades",
    }
    return render(request,'admin/custom/quiz/view_report.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def view_not_attempt(request,pk):
    subjects = Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty).distinct().values_list('subject', flat=True)
    try:
        quiz=Quiz.objects.get(id=pk,subject_assignment__programme__department__degree_category=request.user.faculty.category,subject_assignment__in=subjects)
    except:
        return JsonResponse("Access Denied..!")
   
    attempted_list=qm.Attempt.objects.filter(Quiz=pk).values_list('user')
    students=[]
    #subject_assignments=Subject_Assignment.objects.filter(id__in=subjects)
    subject_assignment=Quiz.objects.filter(id__in=subjects)
    for subject_assignment in quiz.subject_assignment.all(): 
        print(subject_assignment)       
        students += Student.objects.filter(programme__department__degree_category=request.user.faculty.category,programme=subject_assignment.programme).exclude(user__in=attempted_list)
    
    context={
        'students':students,
        'quiz':quiz,
    }
    return render(request,'admin/custom/quiz/view_not_attempt.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_edit_quiz(request,pk):
    user = request.user
    data = dict()
    quiz = Quiz.objects.get(id=pk)
    if request.method == 'POST':
    
        form = QuizForm(request.POST,request=request,instance=quiz)
        if form.is_valid():
            print("hi")
            quiz = form.save(commit=False)
            print(quiz)
            duration=request.POST.get('duration_in_minutes')

            if int(duration) > 0:
                quiz.timed_exam = True
            else:
                quiz.timed_exam = False
            quiz.save()
            form.save_m2m()
            #subjects= Faculty_Subject_Assignment.objects.filter(faculty=user.faculty).distinct().values_list('subject', flat=True)
            subjects= Faculty_Subject_Assignment.objects.filter(faculty=user.faculty).distinct().values_list('subject')
            quizes=Quiz.objects.filter(subject_assignment__in=subjects).distinct().order_by('-openDate')[:6]
            data['valid'] = True            
            data['html'] = render_to_string('admin/custom/quiz/quiz.html',{'quizes':quizes},request)
            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/quiz/quizform.html',{'form':form,'operation':'Update'},request)
        
    else:
        form = QuizForm(request=request,instance=quiz)
        data['form'] = render_to_string('admin/custom/quiz/quizform.html',{'form':form,'operation':'Update','quiz_id':quiz.id},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_delete_home_quiz(request,id):
    user = request.user
    data = dict()
    quiz = Quiz.objects.get(id=id)
    if quiz.created_by == user:
        quiz.delete()
        subject_Assignment = Subject_Assignment.objects.filter(programme=request.user.faculty.programme)
        quizes=Quiz.objects.filter(subject_assignment__in=subject_Assignment).distinct().order_by('-openDate')[:6]
        data['valid'] = True            
        data['html'] = render_to_string('admin/custom/quiz/quiz.html',{'quizes':quizes},request)
           
 
    else:
        data['valid'] = False
        
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_edit_assignment_detail(request,pk):

    user = request.user
    data = dict()
    assignment = Assignment.objects.get(id=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST,request.FILES,request=request,instance=assignment)
        if form.is_valid() and assignment.topic.croom.created_by == user:
            form.save()
            assignments = Assignment.objects.filter(topic__croom__created_by=request.user).order_by('-posted_on')
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/assignment.html',{'assignments':assignments},request)

            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/assignmentform_detail.html',{'form':form,'operation':'Update','assignment_id':pk},request)
        
    else:
        form = AssignmentForm(request=request,instance=assignment)
        data['form'] = render_to_string('admin/custom/assignmentform_detail.html',{'form':form,'operation':'Update','assignment_id':pk},request)
    
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_activate_class(request,pk):
    user = request.user
    data = dict()
    classroom = ClassRoom.objects.get(id=pk)
    if classroom.created_by == user:
        classroom.activate = True
        classroom.save()
        classrooms = ClassRoom.objects.filter(created_by=user).order_by('activate')
        data['valid'] = True
        data['html'] = render_to_string('admin/custom/classrooms.html',{'classrooms':classrooms},request)
    else:
        data['valid'] = False
        
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_add_update(request,model_name,parent_pk=None,pk=None):
    data = dict()
    #classroom = ClassRoom.objects.get(id=parent_pk)
    chapter = Chapter.objects.get(id=parent_pk)
    print("chapter_subject_assignment",chapter.subject_assignment)
    faculty_subject_assignment = Faculty_Subject_Assignment.objects.get(subject=chapter.subject_assignment)
    print("chapter_subject_assignment",faculty_subject_assignment)
    if pk==None:

        
        #if classroom.created_by != request.user:
            #data['html'] = 'Access Denied'
            #return JsonResponse(data)
        if model_name == 'Topic':
            data['model_name'] = 'Topic'
            if request.method == 'POST':
                
                form = TopicForm(request.POST,request.FILES)
                if form.is_valid():
                    topic = form.save(commit=False)
                    topic.chapter = chapter
                    topic.faculty_subject_assignment = faculty_subject_assignment
                    topic.save()
                    topics = Topic.objects.filter(chapter=chapter).order_by('id')

                    data['valid'] = True
                    data['html'] = render_to_string('admin/custom/topics.html',{'topics':topics},request)
                else:
                    data['valid'] = False
                    

            else:
                form = TopicForm()
            
        elif model_name == 'Video':
            data['model_name'] = 'Video'
            if request.method == 'POST':
                
                form = VideoForm(request.POST,request.FILES,request=request,chapter= chapter)
                if form.is_valid():
                    video = form.save()
                    videos = Video.objects.filter(topic__chapter=parent_pk).order_by('-added_on')[:6]

                    data['valid'] = True
                    data['html'] = render_to_string('admin/custom/topic_video.html',{'videos':videos},request)
                else:
                    data['valid'] = False
                    

            else:
                form = VideoForm(request=request,chapter=chapter)
        else:
            data['model_name'] = 'Material'
            if request.method == 'POST':
                
                form = MaterialForm(request.POST,request.FILES,request=request,chapter=chapter)
                if form.is_valid():
                    material = form.save()
                    materials = Material.objects.filter(topic__chapter=parent_pk).order_by('-added_on')[:6]

                    data['valid'] = True
                    data['html'] = render_to_string('admin/custom/topic_material.html',{'materials':materials},request)
                else:
                    data['valid'] = False
                    

            else:
                form = MaterialForm(request=request,chapter=chapter)

        context = {
            'form':form,
            'operation':'Add',
            'model_name':model_name,
            'parent_pk':parent_pk,
             
            }
                
        data['form'] = render_to_string('admin/custom/change_form.html',context,request)
        return JsonResponse(data)
        
    else:
        
        if model_name == 'Topic':
            data['model_name'] = 'Topic'
            topic = Topic.objects.get(id=pk)
            if request.method == 'POST':
                #classroom = ClassRoom.objects.get(id=parent_pk)
                chapter = Chapter.objects.get(id=parent_pk)
                form = TopicForm(request.POST,request.FILES,instance=topic)
                if form.is_valid():
                    topic = form.save()
                    topics = Topic.objects.filter(chapter=chapter).order_by('id')

                    data['valid'] = True
                    data['html'] = render_to_string('admin/custom/topics.html',{'topics':topics},request)
                else:
                    data['valid'] = False
                    

            else:
                form = TopicForm(instance=topic)
            
        elif model_name == 'Video':
            data['model_name'] = 'Video'
            video = Video.objects.get(id=pk)
            if request.method == 'POST':
                
                form = VideoForm(request.POST,request.FILES,request=request,instance=video,chapter=chapter)
                if form.is_valid():
                    video = form.save()
                    videos = Video.objects.filter(topic__chapter=parent_pk).order_by('-added_on')[:6]

                    data['valid'] = True
                    data['html'] = render_to_string('admin/custom/topic_video.html',{'videos':videos},request)
                else:
                    data['valid'] = False
                    

            else:
                form = VideoForm(request=request,instance=video,chapter=chapter)
        else:
            data['model_name'] = 'Material'
            material = Material.objects.get(id=pk)
            if request.method == 'POST':
                
                form = MaterialForm(request.POST,request.FILES,request=request,instance=material,chapter=chapter)
                if form.is_valid():
                    material = form.save()
                    materials = Material.objects.filter(topic__chapter=parent_pk).order_by('-added_on')[:6]

                    data['valid'] = True
                    data['html'] = render_to_string('admin/custom/topic_material.html',{'materials':materials},request)
                else:
                    data['valid'] = False
                    

            else:
                #form = MaterialForm(request=request,instance=material,classroom=classroom)
                form = MaterialForm(request=request,instance=material,chapter=chapter)

        context = {
            'form':form,
            'operation':'Update',
            'model_name':model_name,
            'parent_pk':parent_pk,
            'object_id':pk
             
            }
                
        data['form'] = render_to_string('admin/custom/change_form.html',context,request)
        return JsonResponse(data)


@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_topic_detail(request,pk):
    user= request.user
    topic = Topic.objects.get(id=pk)
    data = dict()
    if topic.croom.created_by == user:
        materials = Material.objects.filter(topic=topic).order_by('-added_on')
        videos = Video.objects.filter(topic=topic).order_by('-added_on')
        data['material_html'] = render_to_string('admin/custom/topic_material.html',{'materials':materials},request)
        data['video_html'] = render_to_string('admin/custom/topic_video.html',{'videos':videos},request)
        return JsonResponse(data)
    else:
        return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_delete(request,model_name,parent_pk,pk):
    
    data = dict()

    chapter = Chapter.objects.get(id=parent_pk)
    #classroom = ClassRoom.objects.get(id=parent_pk)
    #if classroom.created_by != request.user:
            #data['html'] = 'Access Denied'
            #return JsonResponse(data)

    if model_name == 'Topic':
        data['model_name'] = 'Topic'
        topic = Topic.objects.get(id=pk)
        topic.delete()
        topics = Topic.objects.filter(chapter=chapter).order_by('id')
        data['html'] = render_to_string('admin/custom/topics.html',{'topics':topics},request)


    elif model_name == 'Video':
        data['model_name'] = 'Video'
        video = Video.objects.get(id=pk)
        video.delete()
        videos = Video.objects.filter(topic__chapter=chapter).order_by('-added_on')[:6]
        data['html'] = render_to_string('admin/custom/topic_video.html',{'videos':videos},request)


    else:
        data['model_name'] = 'Material'
        material = Material.objects.get(id=pk)
        material.delete()
        materials = Material.objects.filter(topic__chapter=parent_pk).order_by('-added_on')[:6]
        data['html'] = render_to_string('admin/custom/topic_material.html',{'materials':materials},request)

    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_activate_quiz(request,pk):
    user = request.user
    data = dict()
    quiz = qm.Quiz.objects.get(id=pk)
    if qm.Assignment.objects.filter(Quiz=quiz).exists():
        if quiz.created_by == user:
            quiz.isActive = True
            quiz.save()              
            data['valid'] = True
        
        else:
            data['valid'] = False
            data['response'] ="Permission Denied..!"
    else:
        data['valid'] = False
        data['response'] ="No Questions Added..!"

        
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def add_test_question(request,pk):

    quiz = Quiz.objects.get(id=pk)
    if not quiz.created_by == request.user:
        return HttpResponse('Access Denied..!')

    user = request.user
    data = dict()
    
    if request.method == 'POST':      
        
        form = QuestionForm(request.POST or None, request.FILES or None,request=request)
        print(form)
        try:
            parent_question = form.save(commit=False)
            options = NewOptionFormSet(request.POST or None, request.FILES or None,instance=parent_question)
        except:
            options = NewOptionFormSet(request.POST or None, request.FILES or None)
        

        if form.is_valid() and options.is_valid():
            parent_question.created_by=request.user
            #   parent_question.school=request.user.faculty.school
            parent_question.save()          
            options.save()
            qm.Assignment.objects.create(Question=parent_question,marks=1,Quiz_id=pk)
            data['valid'] = True      
            
            
        else:           
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/quiz/question_create_form.html',{'options':options,'form':form,'operation':'Add',})
        return JsonResponse(data)
    else:           
            
        questionform=QuestionForm(request=request)
        options = NewOptionFormSet()
        context = {'options':options,'form':questionform,'operation':'Add','quiz':quiz,}           
         
    return render(request,'admin/custom/quiz/question.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def import_question(request,pk):
    quiz = Quiz.objects.get(id=pk)
    grade_id = request.POST.get('grade')
    subject_id =  request.POST.get('subject')
    print(subject_id)
    data = dict()
    if quiz.created_by == request.user:
        if "POST" == request.method:            
            excel_file = request.FILES["question_file"]         
            error_row=[]
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb["Sheet1"] 
            excel_data = list()           
            for count, row in enumerate(worksheet.iter_rows()):               
                if count == 0:
                    continue
                elif row[0].value == 'end':
                    break

                question_description=str(row[1].value).replace('\n','<br>')
                answer_description=str(row[2].value).replace('\n','<br>')
                
                row_data = list() 
                print("testbuddy",subject_id)               
                subject=Subject_Assignment.objects.get(id=subject_id)
                print("subjctetest",subject.subject)
                grade = Programme.objects.get(id=grade_id)
                #subject_assignment = Subject_Assignment.objects.filter(programme=grade)
                print("q",grade)
                print("q112",subject)

                if row[0].value == None or  row[7].value == None or  row[1].value == None:
                    error_row.append("row " + str(count+1))
                    continue
                

                q = qm.Question(name=row[0].value,description=question_description,answer_description=answer_description,subject=subject.subject,created_by=request.user)
                q.save()


                for  i in range(3,7):  
                    option_description=str(row[i].value).replace('\n','<br>')                               
                    if (i+2)-4 == int(row[7].value):                        
                        o = qm.Option(name=option_description,value=1.0,Question=q)
                    else:
                        o = qm.Option(name=option_description,value=0,Question=q)

                    try:
                        if row[i].value != None:
                            o.save()
                        
                    except:
                        qm.Option.objects.filter(question=q).delete()
                        qm.Question.objects.filter(id=q).delete()
                        error_row.append(row[0].value )
                        continue

                
                assignment = qm.Assignment.objects.create(Quiz=quiz,Question=q)
               

                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)

            
            data['valid'] = True
            data['status'] = render_to_string('admin/custom/quiz/import_question_status.html',{'excel_data':excel_data,'error_rows':error_row,},request)
            data['assigned_questions'] = render_to_string('admin/custom/quiz/quiz_assignment.html',{'quiz':quiz,},request)
            
        else:
            data['valid'] = False
    else:
        data['valid'] = False

    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def load_question(request):
    data = dict()
    subject = int(request.GET.get('subject'))
    #subject_assignment = request.GET.get('subject')
    subject_assignment = Subject_Assignment.objects.filter(subject__id=subject)
    print(subject_assignment)
    grade = request.GET.get('grade')
    print("test-grade",grade)
    quiz = request.GET.get('quiz')
    get_assigned_questions=qm.Assignment.objects.filter(Quiz=quiz).values_list('Question', flat=True)
    print(get_assigned_questions)
    if grade:
        print(subject,subject_assignment)
        #question = qm.Question.objects.filter(subject_assignment__programme=grade,subject_assignment=subject_assignment).exclude(id__in=get_assigned_questions)
        question = qm.Question.objects.filter(subject__id=subject).exclude(id__in=get_assigned_questions)
        print(question)
        context={
            
            'questions' : question,       
            
        }
        data['question'] = render_to_string('admin/custom/quiz/question_fly.html', context) 
    else:
        data['error'] = "Something went Wrong"
    return JsonResponse(data)



@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_search_questions(request):
    
    data = dict()
    subject = int(request.GET.get('subject'))
    grade = request.GET.get('grade')
    print(grade)
    question = request.GET.get('question')
    quiz = request.GET.get('quiz')
    get_assigned_questions=qm.Assignment.objects.filter(Quiz=quiz).values_list('Question', flat=True)
    if grade:
        print("test-grate",grade,subject,question)
        question = qm.Question.objects.filter(description__icontains = question).exclude(id__in=get_assigned_questions)   
        print(question)   
        context={
            
            'questions' : question,       
            
        }
        data['question'] = render_to_string('admin/custom/quiz/question_fly.html', context) 
        data['question_count'] = question.count()
    else:
        data['error'] = "Something went Wrong"
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_question_assign(request):
    data=dict()
    mark=request.GET.get('mark')  
    quiz_id=request.GET.get('quiz_id')
    questions=request.GET.get('question')

    questions=json.loads(questions)
    questions = [x.strip() for x in questions.split(',')]
    for question in questions:   
        question=qm.Question.objects.get(id=question)
        quiz=qm.Quiz.objects.get(id=quiz_id)
     
        qm.Assignment.objects.create(Question=question,Quiz=quiz,marks=mark)
        data['status'] = "Done"      

    return JsonResponse(data)


@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def edit_question(request,pk,quizid):
    user = request.user
    data = dict()
    question = qm.Question.objects.get(id=pk)
    quiz = Quiz.objects.get(id=quizid)
    if not (question.created_by == request.user and quiz.created_by == request.user):
        return HttpResponse("Access Denied..!")
    if request.method == 'POST':
        form = QuestionForm(request.POST or None, request.FILES or None, instance=question,request=request)
        options = OptionFormSet(request.POST or None, request.FILES or None, instance=question)

        if form.is_valid() and options.is_valid():
            form.save()
            options.save()
            data['valid'] = True
           
        else:           
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/quiz/question_create_form.html',{'options':options,'form':form,'question':question,'quiz':quiz,})
        
        return JsonResponse(data)
    else:    
        questionform=QuestionForm(request=request,instance=question)
        options = OptionFormSet(instance=question)            
        context = {'options':options,'form':questionform,'operation':'Update','quiz': quiz,'question':question,}
          
    return render(request,'admin/custom/quiz/question.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_edit_quiz_assignment(request,pk):
    user = request.user
    data = dict()
    assignment = qm.Assignment.objects.get(id=pk)
    if request.method == 'POST':
        form = QuizAssignmentForm(request.POST,request=request,instance=assignment)
        if form.is_valid() and assignment.Question.created_by == user:
            form.save()
            quiz = quiz=Quiz.objects.get(id=assignment.Quiz.id)
            data['valid'] = True
            data['html'] = render_to_string('admin/custom/quiz/quiz_assignment.html',{'quiz':quiz},request)
            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/assignmentform.html',{'form':form,'operation':'Update','assignment_id':pk},request)
        
    else:
        form = QuizAssignmentForm(request=request,instance=assignment)
        data['form'] = render_to_string('admin/custom/quiz/quiz_assignmentform.html',{'form':form,'operation':'Update','assignment_id':pk},request)
    return JsonResponse(data)

#Quiz
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization 
def ajax_delete_quiz_question(request,pk):
    user = request.user
    data = dict()
    assignment = qm.Assignment.objects.get(id=pk)    
    assignment.delete() 
    data['valid'] = True       
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def delete_post(request,pk):
    forum = Forum.objects.get(id=pk) 
    if forum.topic.croom.created_by == request.user:
        forum.delete()
    return redirect('faculty_classroom')

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_post_reply(request,pk):
    data = dict()
    forum = Forum.objects.get(id=pk) 
    form = ReplyForm(request.POST)
    
    if form.is_valid() :
        reply = form.save(commit=False)
        reply.forum = forum
        reply.posted_by = request.user
        reply.save()
        replies = Reply.objects.get(id=reply.id)
        data['valid'] = True
        data['html'] = render_to_string('admin/custom/reply.html',{'reply':reply},request)
        
    else:
        data['valid'] = False
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def ajax_delete_reply(request,pk):
    data = dict()
    reply = Reply.objects.get(id=pk)
    if reply.forum.topic.croom.created_by == request.user:
        reply.delete()
        data['valid'] = True
    else:
        data['valid'] = False
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def assignment_correction(request,pk):
    submission=Submission.objects.get(id=pk,student__programme=request.user.faculty.programme,assignment__topic__faculty_subject_assignment__faculty__user=request.user)
    if request.method == 'POST':        
        form = SubmissionForm(request.POST,request.FILES, instance=submission)
        data=dict()
        if form.is_valid():     
       
            form.save()
            return redirect('view_submission',pk=submission.assignment.id)

            
        else:
            data['valid'] = False
            data['form'] = render_to_string('admin/custom/correction.html',{'form':form,'operation':'Add'},request)
        

        return JsonResponse(data)
        
    else:
        
        form = SubmissionForm(instance=submission)
        context={
            'submission' : submission,
            'form': form,
          }
        return render(request,'admin/custom/correction.html',context)
    
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def mark_submission(request,pk):
    submission = Submission.objects.get(id=pk)
    if submission.assignment.topic.faculty_subject_assignment.faculty.user == request.user:
        submission.status = request.POST['status']
        submission.marks = request.POST['marks']
        submission.save()
        return redirect('view_submission',pk=submission.assignment.id)
    return HttpResponse('Access Denied')

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def save_cfile(request,pk):
    if request.method == "POST":
        data = dict()
        pdf = request.FILES['cfile']    
        submission = Submission.objects.get(id=pk)     
        if submission.assignment.topic.croom.created_by == request.user:
             submission.sfile=pdf
             submission.save()
             data['valid'] = True
        else:
            data['valid'] = False
        return JsonResponse(data)
#Resource Management
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def faculty_resource_list(request):
    resources = Resource.objects.filter(subject_assignment__programme__department__degree_category=request.user.faculty.category)
    context={     
        'resources':resources,
    }
    return render(request,'faculty/resource_list.html',context)

def faculty_video_list(request,id):
    resource = Resource.objects.get(id=id)
    videos = Re_Video.objects.filter(resource=resource).order_by('-id')
    context={     
        'resource':resource,
        'videos':videos,
    }
    return render(request,'faculty/faculty_video_list.html',context)

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def faculty_add_video(request,pk):
    resource = Resource.objects.get(id=pk,subject_assignment__programme__department__degree_category=request.user.faculty.category)
    data = dict()
    if request.method == "POST":
        form = Re_VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.resource=resource
            video.save()
            videos = Re_Video.objects.filter(resource=resource).order_by('-id')
            data['html'] = render_to_string('faculty/video.html',{'videos':videos},request)
            data['valid'] = True

        else:
            context = {
                'form':form,
                'operation':'Add',
                'pk':pk,
            }
            data['form'] = render_to_string('faculty/video_form.html',context,request)
            data['valid'] = False

    else:
        form = Re_VideoForm()
        context = {
            'form':form,
            'operation':'Add',
            'pk':pk,
        }        
        data['form'] = render_to_string('faculty/video_form.html',context,request)
        data['valid'] = True

    return JsonResponse(data) 

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def faculty_edit_video(request,pk):
    data = dict()
    video = Re_Video.objects.get(id=pk,resource__subject_assignment__programme__department__degree_category=request.user.faculty.category)
    if request.method == "POST":
        form = Re_VideoForm(request.POST,instance=video)
        if form.is_valid():
            form.save()
            videos = Re_Video.objects.filter(resource=video.resource).order_by('-id')
            data['html'] = render_to_string('faculty/video.html',{'videos':videos},request)
            data['valid'] = True
        else:
            context = {
                'form':form,
                'operation':'Update',
                'pk':pk,
            }
            
            data['form'] = render_to_string('faculty/video_form.html',context,request)
            data['valid'] = False

    else:
        form = Re_VideoForm(instance=video)
        context = {
            'form':form,
            'operation':'Update',
            'pk':pk,
        }        
        data['form'] = render_to_string('faculty/video_form.html',context,request)
        data['valid'] = True

    return JsonResponse(data) 

@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def faculty_video_delete(request,pk):
    data = dict()
    video = Re_Video.objects.get(id=pk,resource__subject_assignment__programme__department__degree_category=request.user.faculty.category)
    resource =video.resource 
    if video:
        video.delete()  
        videos = Re_Video.objects.filter(resource=resource).order_by('-id')
        data['html'] = render_to_string('faculty/video.html',{'videos':videos},request)
        data['valid'] = True
    else:
        data['valid'] = False
    return JsonResponse(data) 

def add_resource(request):
    data = dict()
    if request.method == 'POST':
        form = ResourceForm(request.POST,request.FILES or None)
        if form.is_valid:
            form_1 = form.save(commit=False)
            form_1.posted_by = request.user
            form_1.posted_on = date.today()
            form_1.save()
            form.save_m2m()
            resources = Resource.objects.filter(subject_assignment__programme__department__degree_category=request.user.faculty.category)
            data['html'] = render_to_string('faculty/resource.html',{'resources':resources},request)
            data['valid'] = True
            return JsonResponse(data)
        else :
            form = ResourceForm()
            context={
                'form':form,
                'operation':'Add',
            }
            data['form'] = render_to_string('faculty/add_resource.html',context,request)
            data['valid'] = True
            return JsonResponse(data) 
    else:        
        form = ResourceForm()
        context={
            'form':form,
            'operation':'Add',
        }
        data['form'] = render_to_string('faculty/add_resource.html',context,request)
        data['valid'] = True
        return JsonResponse(data) 

def edit_resource(request,id):
    resource = Resource.objects.get(id=id)
    data =dict()
    if request.method == 'POST':
        form = ResourceForm(request.POST,request.FILES or None,instance=resource)
        print(form)
        if form.is_valid:
            form_resource = form.save(commit=False)
            form_resource.posted_by = request.user
            form_resource.posted_on = date.today()
            form_resource.save()
            form.save_m2m()
            resources = Resource.objects.filter(subject_assignment__programme__department__degree_category=request.user.faculty.category)
            data['html'] = render_to_string('faculty/resource.html',{'resources':resources},request)
            data['valid'] = True
            return JsonResponse(data)
        else :
            form = ResourceForm(instance=resource)
            print(resources)
            context={
                'form':form,
                #'operation':'Update',
                'resource':resource,
            }
            data['form'] = render_to_string('faculty/add_resource.html',context,request)
            data['valid'] = True
            return JsonResponse(data) 
    else:       
        form = ResourceForm(instance=resource)
        context={
            'form':form,
            #'operation':'Update',
            'resource':resource,
        }
        data['form'] = render_to_string('faculty/add_resource.html',context,request)
        data['valid'] = True
        return JsonResponse(data) 
    
def delete_resource(request,id):
    resource = Resource.objects.get(id=id)
    data =dict()
    if resource:
        resource.delete()
        resources = Resource.objects.filter(subject_assignment__programme__department__degree_category=request.user.faculty.category)    
        data['html'] = render_to_string('faculty/resource.html',{'resources':resources},request)
        data['valid'] = True
        return JsonResponse(data)  
    else:
        data['valid'] = False
        return JsonResponse(data)
    
#Load Section
@login_required(login_url='login') #Authentication
@user_passes_test(is_faculty,login_url='login') #Authorization
def load_section(request,pk,model_name):
    data = dict()
    if model_name == "classroom":
        sections = list(Faculty_Subject_Assignment.objects.filter(faculty=request.user.faculty,subject__id=pk).distinct().values_list('section'))
        sections = sections[0]
        data['section'] = render_to_string('admin/custom/load_section.html',{'sections':sections,},request)
        data['valid'] = True
    else:
        data['valid'] = False

    return JsonResponse(data)