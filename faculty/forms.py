from operator import imod
from django import forms
from general.models import Subject
from virtual_class.models import ClassRoom,Assignment,Upcoming_Session,Submission,Topic,Material, Video
from general.models import Subject_Assignment
from quiz import models as qm
from quiz.models import Quiz,Question,Option
from ckeditor.fields import RichTextField
from .models import Log_Book,Log_Book_Entry
from django.forms.models import inlineformset_factory

class ClassRoomForm(forms.ModelForm):
    
    class Meta:
        model = ClassRoom
        fields = ('name','subject_assignment')
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")  
        super(ClassRoomForm, self).__init__(*args, **kwargs) 
        subject_category= self.request.user.faculty.subject_category
        self.fields['subject_assignment'].queryset = Subject_Assignment.objects.filter(programme=self.request.user.faculty.programme,programme__department__degree_category=self.request.user.faculty.category,programme__graduation__code=self.request.user.faculty.graduation)    
        #self.fields['subject_assignment'].queryset = Subject_Assignment.objects.filter(subject__subject_category=subject_category,programme__department__degree_category=self.request.user.faculty.category,programme__graduation__code=self.request.user.faculty.graduation)
        self.fields["subject_assignment"].choices = [("", "Choose Subject Assignment"),] + \
                list(self.fields["subject_assignment"].choices)[1:]
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
     
class AssignmentForm(forms.ModelForm):
    due_date=forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ) )

    class Meta:
        model = Assignment
        fields = ('title','topic','due_date','afile','marks')
        
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(faculty_subject_assignment__faculty__user=self.request.user)
        self.fields['topic'].choices = [("", "Choose Topic"),] + \
                list(self.fields["topic"].choices)[1:]
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Upcoming_SessionForm(forms.ModelForm):
    start_date=forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ))
    start_time=forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'} )) 
    class Meta:
        model = Upcoming_Session
        exclude = ('end_date',)
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        super(Upcoming_SessionForm, self).__init__(*args, **kwargs)
        self.fields['classroom'].queryset = ClassRoom.objects.filter(created_by=self.request.user)
        self.fields["classroom"].choices = [("", "Choose Classroom"),] + \
                list(self.fields["classroom"].choices)[1:]
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class QuizForm(forms.ModelForm):
    openDate=forms.DateField(label="Open Date", widget=forms.TextInput(attrs={'type': 'date'} ) )
    closeDate=forms.DateField(label="Close Date", widget=forms.TextInput(attrs={'type': 'date'} ) )

    class Meta:
        model = Quiz
        fields = ('name','openDate','closeDate','duration_in_minutes','subject_assignment')
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['duration_in_minutes'].required = True
        subject_category= self.request.user.faculty.subject_category
        self.fields['subject_assignment'].queryset = Subject_Assignment.objects.filter(programme=self.request.user.faculty.programme,programme__department__degree_category=self.request.user.faculty.category,programme__graduation__code=self.request.user.faculty.graduation)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'   
#logbook

class Log_Book_Form(forms.ModelForm):
    answer_description=RichTextField()

    class Meta:
        model = Log_Book
        exclude = ('subject',)

    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        super(Log_Book_Form, self).__init__(*args, **kwargs)
        

class Log_Book_Entry_Form(forms.ModelForm):
    content_delivered = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))
    activity = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))

    class Meta:
        model = Log_Book_Entry
        exclude = ('log_book',)  
        fields = ('hour','chapter','content_delivered','activity')



Log_Book_Entry_FormSet = inlineformset_factory(Log_Book, Log_Book_Entry,
                                            form=Log_Book_Entry_Form, extra=9,can_delete = False,max_num=9)


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('status','marks','corrected_answer_sheet')

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title',)
        
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'link', 'topic')

    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        self.chapter = kwargs.pop("chapter")
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(chapter=self.chapter)
        self.fields["topic"].choices = [("", "Choose Topic"),] + \
                list(self.fields["topic"].choices)[1:]
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('title', 'material', 'topic')

    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        self.chapter = kwargs.pop("chapter")
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(chapter=self.chapter)
        self.fields["topic"].choices = [("", "Choose Topic"),] + \
                list(self.fields["topic"].choices)[1:]
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
                

class QuestionForm(forms.ModelForm):
    answer_description=RichTextField()

    class Meta:
        model = Question
        exclude = ('created_by',)
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuestionForm, self).__init__(*args, **kwargs)
        subject_assignment=Subject_Assignment.objects.filter(programme=self.request.user.faculty.programme,programme__graduation__code=self.request.user.faculty.graduation)
        self.fields['subject_assignment'].queryset = subject_assignment
        subject =Subject.objects.filter(subject_category=self.request.user.faculty.subject_category,degree_categaroy=self.request.user.faculty.category)
        self.fields['subject'].queryset = subject
        #self.fields["subject_assignment"].choices = [("", "Choose"),] + \
                #list(self.fields["subject_assignment"].choices)
                
        #subjects= Subject_Assignment.objects.filter(subject__subject_category=self.request.user.faculty.subject_category).values_list('subject',flat=True).distinct()
        #self.fields['subject'].queryset = Subject.objects.filter(id__in=subjects)
        #self.fields["subject"].choices = [("", "Choose Subject"),] + \
                #list(self.fields["subject"].choices)[1:]
        #self.fields['description'].label = "Question Statement"
        

class OptionForm(forms.ModelForm):
 
    class Meta:
        model = Option
        exclude = ('Question',)
        


class QuizAssignmentForm(forms.ModelForm):
    class Meta:
        model = qm.Assignment
        exclude = ()  
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuizAssignmentForm, self).__init__(*args, **kwargs)
        subjects = self.request.user.teacher.subjects
        self.fields['Quiz'].queryset = Quiz.objects.filter(school=self.request.user.teacher.school,subjects__in=subjects).distinct().order_by('-openDate')
        self.fields["Quiz"].choices = [("", "Choose Quiz"),] + \
                list(self.fields["Quiz"].choices)[1:]


        self.fields['Question'].queryset = Question.objects.filter(created_by=self.request.user).order_by('-id')
        self.fields["Question"].choices = [("", "Choose Question"),] + \
                list(self.fields["Question"].choices)[1:]
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


OptionFormSet = inlineformset_factory(Question, Option,
                                            form=OptionForm, extra=2)


NewOptionFormSet = inlineformset_factory(Question, Option,
                                            form=OptionForm, extra=4)
