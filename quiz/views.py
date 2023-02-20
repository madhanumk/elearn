from re import sub
from django.shortcuts import render
from general.models import Subject_Assignment, Subject
from .models import Quiz,Attempt,On_Test,Assignment,Question
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from datetime import datetime, date, timedelta
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from general.views import is_student, is_stud_faculty_user, is_faculty
from django.shortcuts import redirect
import json
from django.views.generic.edit import FormView
from django.db.models import Q
from .forms import QuizForm,ResponseForm
from django.template.loader import render_to_string
# Create your views here.

class QuizListView(LoginRequiredMixin,ListView):
    model=Quiz
    login_url = 'login'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        
        return context
    
    def get_queryset(self):
        #stud = request.user.student
        attempted = Attempt.objects.filter(user=self.request.user).values_list('Quiz',flat=True)
        subjects = Subject_Assignment.objects.filter(programme__department__degree_category__id=self.request.user.student.department.degree_category.id).values_list('id',flat=True)
        return Quiz.objects.filter(subjects__in=subjects,openDate__lte=datetime.today(), closeDate__gte=datetime.today()).order_by('-openDate').exclude(id__in=attempted)
    


class QuizDetail(SingleObjectMixin,LoginRequiredMixin,ListView):
    paginate_by = 1
    template_name = "quiz/quiz_detail.html"
    login_url = 'login'
       
    def get(self, request, *args, **kwargs):
        current_user = request.user
       
        if  Attempt.objects.filter(user=self.request.user,Quiz=self.kwargs['pk']).values_list('Quiz',flat=True).exists():
            return HttpResponse("No More attempts allowed")       

        if not On_Test.objects.filter(user=request.user).exists():
            On_Test.objects.create(user=request.user,test_id=self.kwargs['pk'],started_time=datetime.now())

        old_one=[]

        current_test=Quiz.objects.get(id=self.kwargs['pk'])
        old_test=On_Test.objects.get(user=request.user)   
 
        if current_test.id == old_test.test.id:
            if not current_test.timed_exam:
                self.mins = None
                self.seconds = None

            else:
                then = old_test.started_time
                now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S') 
                diff = (now - then).total_seconds()       
                self.mins = current_test.duration_in_minutes - ((diff // 60) + 1)
                self.seconds = 59 - diff % 60

            if request.user.groups.filter(name='Student').exists():
                self.object = self.get_object(queryset=Quiz.objects.filter((Q(subject_assignment__programme__department__degree_category__id=request.user.student.programme.department.degree_category.id)), openDate__lte=date.today(), closeDate__gte=date.today()))
                print("self",self.object)
                
            elif request.user.groups.filter(name='faculty').exists():
                subjects = request.user.faculty
                self.object = self.get_object(queryset=Quiz.objects.filter((Q(subject_assignment__programme__department__degree_category__id=request.user.faculty.programme.department.degree_category.id)),openDate__lte=date.today(), closeDate__gte=date.today()).distinct())

            self.questions=list(Assignment.objects.filter(Quiz=self.object.id).values_list('Question_id', flat=True))
            self.assignment = Assignment.objects.get(Quiz=self.object.id,Question=self.questions[0])
            print("s-q",self.questions)

        else:
            return  render(request, 'quiz/old_test.html', {'old_test':old_test,'current_test':current_test,})
    

        return super().get(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context={
                'quiz' : self.object,
                'question_count' : len(self.questions),
                'question_no' : 0,
                'assignment' : self.assignment,
                'questions' : self.questions,
                'question_next' : 1,
                'question_prev' : -1,
                'mins':self.mins,
                'seconds':self.seconds,
                
            
        }              
        return context
    
        
    def get_queryset(self):       
        return "Query set"
     
           
    def post(self,request, *args, **kwargs):                
        return HttpResponseRedirect('/')

@login_required(login_url='login')
def quiz_load_question(request):
    data = dict()
    no = int(request.GET.get('question_no'))
    test = request.GET.get('test')
   
    #get test questions
    test_object=Quiz.objects.get(id=test)

    questions=list(Assignment.objects.filter(Quiz=test_object).values_list('Question_id', flat=True))
    
    assignment = Assignment.objects.get(Quiz=test_object,Question=questions[no])
   
                   
    context={     

            'assignment' : assignment,
            'test':test_object,
            'question_no': no,           
              
        }
    print("no",assignment)
    data['question'] = render_to_string('quiz/quiz_questions_fly.html', context)
    print("no",data['question'])     
    data['question_no'] = no
    data['question_id'] = assignment.Question.id
    data['question_count'] = len(questions)

    return JsonResponse(data)




@login_required(login_url='login') #Authentication
@user_passes_test(is_stud_faculty_user,login_url='login') #Authorization    
def quizsubmit(request):
    json_data=json.loads(request.body.decode('utf-8'))
    data = dict()
    current_user = request.user
    quiz_id=int(json_data[0]['quizid'])
    
    quiz = Quiz.objects.get(id=quiz_id)   
    if len(json_data)==1 and not 'questionid' in json_data[0]:
        Attempt.objects.create(user=current_user,Quiz=quiz,score=0)
        score=0
        On_Test.objects.filter(user=current_user,test=quiz).delete()
    else:
        score = Attempt.Create(quiz_id,current_user,json_data)
    
    data['score'] = score
    return JsonResponse(data)

@login_required(login_url='login') #Authentication
@user_passes_test(is_stud_faculty_user,login_url='login') #Authorization
def my_scores(request):
    if is_student(request.user):
        subjects = Subject_Assignment.objects.filter(programme=request.user.student.programme,semester=request.user.student.semester,year=request.user.student.year)
        Attempts = Attempt.objects.filter(user=request.user,Quiz__subject_assignment__in=subjects.all()).order_by('-date').distinct()
    elif is_faculty(request.user):        
        subjects= request.user.faculty.programme.title
        print(subjects)
        #Attempts = Attempt.objects.filter(user=request.user,Quiz__subject_assignment__programme__title__in=subjects).order_by('-date').distinct()
        Attempts = Attempt.objects.filter(user=request.user).order_by('-date').distinct()
    print(Attempts)
    return render(request,'quiz/my_scores.html',{'Attempts':Attempts,'subjects':subjects})
    
@login_required(login_url='login') #Authentication
@user_passes_test(is_stud_faculty_user,login_url='login') #Authorization
def filter_scores(request):
    data = dict()
    subject = request.GET.get('subject')
    print("scorefilter")
    Attempts = Attempt.objects.filter(user=request.user,Quiz__subject_assignment=subject).order_by('-date')
    data['html_scores'] = render_to_string('quiz/scores.html',{'Attempts':Attempts},request=request)
    return JsonResponse(data)

class QuizView(FormView):
    template_name = 'quiz/addquiz.html'
    form_class = QuizForm
    success_url = '/'
    model=Quiz

    
    def form_valid(self, form):        
        form.save()
        return super().form_valid(form)

def manage_quiz(request,quiz_id):
    '''author = Assignment.objects.get(Quiz__id=quiz_id)
    QuizInlineFormSet = inlineformset_factory(Assignment, Response, fields=('option',))
    if request.method == "POST":
        formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(author.get_absolute_url())
    else:
        formset = BookInlineFormSet(instance=author)
    return render(request, 'manage_books.html', {'formset': formset})'''
'''@login_required(login_url='login')
def ques_upload(request):
    if request.user.username == "admin":
        if "GET" == request.method:
            return render(request, 'quiz/quest.html', {})
        else:
            excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

            wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            print(worksheet)

            excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
            for row in worksheet.iter_rows():
                row_data = list()
                q = Question(name=row[0].value,description=row[1].value,answer_description=row[2].value)
                q.save()

                for i in range(3,len(row),2):
                    o = Option(name=row[i].value,value=row[i+1].value,Question=q)
                    o.save()

                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)

            return render(request, 'quiz/quest.html', {"excel_data":excel_data})
    else:
        return render(request, 'quiz/quest.html', {})'''


class QuizAnswerDetail(SingleObjectMixin,LoginRequiredMixin,ListView):
    template_name = "quiz/answer_detail.html"
    login_url = 'login'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        current_user = request.user    
        self.object=self.get_object(queryset=Quiz.objects.all())
        if not Attempt.objects.filter(user=request.user,Quiz=self.object).exists():
            return redirect('home')
        return super().get(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.object
       
        return context

    
    def get_queryset(self):
        return self.object.assignment_set.all()





@login_required(login_url='login')
def load_question(request):
    data = dict()
    subject = int(request.GET.get('subject'))
    grade = request.GET.get('grade')
    quiz = request.GET.get('quiz')
    get_assigned_questions=Assignment.objects.filter(Quiz=quiz).values_list('Question', flat=True)

    if grade:
        if request.user.groups.filter(name='School').exists():
            question = Question.objects.filter(grade__grade=grade,subject=subject,school=request.user.school).exclude(id__in=get_assigned_questions)
        elif request.user.groups.filter(name='Teacher').exists():
            question = Question.objects.filter(grade__grade=grade,subject=subject,created_by=request.user).exclude(id__in=get_assigned_questions)

        context={
            
            'questions' : question,       
            
        }
        data['question'] = render_to_string('quiz/question_fly.html', context) 
    else:
        data['error'] = "Something went Wrong"
    return JsonResponse(data)



@login_required(login_url='login')
def ajax_search_questions(request):

    data = dict()
    subject = int(request.GET.get('subject'))
    grade = request.GET.get('grade')
    question = request.GET.get('question')
    quiz = request.GET.get('quiz')
    get_assigned_questions=Assignment.objects.filter(Quiz=quiz).values_list('Question', flat=True)
    print("AJAA get serach")
    if grade:
        
        if request.user.groups.filter(name='College').exists():
            print("school")
            question = Question.objects.filter(subject=subject,description__icontains = question,school=request.user.school).exclude(id__in=get_assigned_questions)
        elif request.user.groups.filter(name='Faculty').exists():
            print("Teacher")
            question = Question.objects.filter(subject=subject,description__icontains = question,created_by=request.user).exclude(id__in=get_assigned_questions)   
        print(question)      
        context={            
            'questions' : question,
        }
        data['question'] = render_to_string('quiz/question_fly.html', context) 
        data['question_count'] =question.count()

    else:
        data['error'] = "Something went Wrong"
    return JsonResponse(data)




@login_required(login_url='login')
def ajax_load_subjects(request):
    data=dict()
    programme=request.GET.get('grade')
    print("degree",programme)
    subjets = Subject_Assignment.objects.filter(programme=programme).values_list('subject', flat=True).distinct()            
    print("testoo",subjets)
    subjects = Subject.objects.filter(id__in=subjets) 
    print(subjects)
    context={            
            'subjects' : subjects,    
        }
    data['subjects'] = render_to_string('quiz/choose_subjects.html', context)  
    return JsonResponse(data)


def delete_on_test(request,test):
    On_Test.objects.filter(user=request.user,test=test).delete()
    data = dict()
    data['status'] = 'done'       
    return JsonResponse(data)