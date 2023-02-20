from django.db import models
from django.db.models import Sum
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import datetime
from general import models as gm


class Quiz(models.Model):
    name = models.CharField(max_length=30)
    openDate = models.DateField(verbose_name='Open Date')
    closeDate = models.DateField(verbose_name='Close Date')    
    #subjects = models.ManyToManyField(gm.Subject)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    timed_exam=models.BooleanField(default=False)
    duration_in_minutes=models.PositiveIntegerField(null=True,blank=True)
    subject_assignment = models.ManyToManyField(gm.Subject_Assignment)
    isActive= models.BooleanField()

 
    def __str__(self):
        return self.name

    @property
    def subject(self):        
        return self.subjects.all()


    @property
    def strength(self):
        total=0     
        
        grade=gm.Subject_Assignment.objects.filter(id__in=self.subject_assignment.all()).values('programme')   
        grades=gm.Programme.objects.filter(id__in=grade)
        for grade in grades:
            total += gm.Student.objects.filter(programme=grade).count()
        
            
            
            #print(subjects.grade)
        #count = Student.objects.filter(school=self.created_by.teacher.school,board=self.created_by.teacher.school.board,grade=self.topic.croom.subject.grade).count()
        return total

    @property
    def submitted_count(self):
        count = Attempt.objects.filter(Quiz__id=self.id).exclude(user__groups__name="Faculty").count()
        return count
    def question_count(self):
        count = Assignment.objects.filter(Quiz__id=self.id).count()
        return count

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Test'

class Question(models.Model):
    name = models.CharField(max_length=30)
    description=RichTextUploadingField()
    answer_description=RichTextUploadingField(null=True,blank=True)
    subject = models.ForeignKey(gm.Subject, on_delete=models.CASCADE,null=True)
    subject_assignment = models.ManyToManyField(gm.Subject_Assignment)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    
    def __str__(self):
        return self.name
    @property
    def options(self):
        return self.option_set.values()
    
    @property
    def answers(self):
        return self.option_set.filter(value__gt=0.0)

class On_Test(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    started_time=models.DateTimeField(null=True)
    
    
    class Meta:
        verbose_name = 'Live Test'
        verbose_name_plural = 'Live Test'

    

class Option(models.Model):
    name = RichTextUploadingField(null=True,blank=True)
    value= models.FloatField(default=0)
    Question=models.ForeignKey(Question,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Assignment(models.Model):      
    Question=models.ForeignKey(Question,on_delete=models.CASCADE)
    marks=models.IntegerField(default=1) 
    Quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)

    def __str__(self):
        return self.Quiz.name + "-" + self.Question.name
        
    class Meta:
        verbose_name = 'Test Question'
        verbose_name_plural = 'Test Question'
        ordering = ['-id']


class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)

    #Getter Methods

    def user_name(self):
        return self.user.first_name

    def user_section(self):
        if self.user.groups.filter(name='Student').exists():
            return self.user.student.section
        else:
            return None
    
    def quiz_name(self):
        return  self.Quiz.name

    def user_full_name(self):
        return  self.user.get_full_name()

    def user_grade(self):
        return  self.user.student.grade

    def rank(self):
        obj=Attempt.objects.get(user=self.user,id=self.id,Quiz=self.Quiz)
        rank = Attempt.objects.filter(score__gt=obj.score,Quiz=self.Quiz).count()
        return rank+1

       
    @classmethod
    def Create(self,Quizid,user,data):
        quiz = Quiz.objects.get(id=Quizid)
        attempt=self(user=user,Quiz=quiz)
        attempt.save()
        objs = (Response(user=user,Option=Option.objects.get(id=data[i]['optionid']),Assignment=Assignment.objects.get(id=data[i]['assignmentid']),Attempt=attempt) for i in range(len(data)))
        response = list(objs)
        Response.objects.bulk_create(response)
        total_attended=0
        total=0
        

        for i in range(len(data)):
            a=Assignment.objects.get(id=data[i]['assignmentid'])
            o=Option.objects.get(id=data[i]['optionid'])
            total_attended=total_attended+(a.marks*o.value)
            #total=total+a.questionValue
        total=Assignment.objects.filter(Quiz=Quizid).aggregate(Sum('marks')).get('marks__sum')
        total=(total_attended/total)*100

        Attempt.objects.filter(id=attempt.id).update(score=total)
        On_Test.objects.filter(user=user,test=Quizid).delete()
        
        if quiz.name == "VAK Learning Style":
            a_count = Response.objects.filter(user=user,Attempt=attempt,Option__value=-1).count()
            b_count = Response.objects.filter(user=user,Attempt=attempt,Option__value=0).count()
            c_count = Response.objects.filter(user=user,Attempt=attempt,Option__value=1).count()

            if (a_count >= b_count) and (a_count >= c_count):
                ls = gm.Learning_Style(student=user.student,learning_style="Visual")
                ls.save()
            if (b_count >= a_count) and (b_count >= c_count):
                ls = gm.Learning_Style(student=user.student,learning_style="Auditory")
                ls.save()
            if (c_count >= a_count) and (c_count >= b_count):
                ls = gm.Learning_Style(student=user.student,learning_style="Kinaesthetic")
                ls.save()
        
        return total
    
    @classmethod
    def Create_Survey(self,Quizid,user,data):
        quiz = Quiz.objects.get(id=Quizid)
        
        attempt=self(user=user,Quiz=quiz)
        attempt.save()
        objs = (Response(user=user,Option=Option.objects.get(id=data[i]['optionid']),Assignment=Assignment.objects.get(id=data[i]['assignmentid']),Attempt=attempt) for i in range(len(data)))
        response = list(objs)
        Response.objects.bulk_create(response)


class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Option=models.ForeignKey(Option,on_delete=models.CASCADE)
    Assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    Attempt=models.ForeignKey(Attempt,on_delete=models.CASCADE)

    '''def bulkadd(user,attempt,data):

        objs = (Response(user=user,Option=Option.objects.get(id=data[i]['optionid']),Assignment=Assignment.objects.get(id=data[i]['assignmentid']),Attempt=attempt) for i in range(len(data)))
        response = list(objs)
        Response.objects.bulk_create(response)
        total=0

        for i in range(len(data)):
            a=Assignment.objects.get(id=data[i]['assignmentid'])
            o=Option.objects.get(id=data[i]['optionid'])
            total=total+(a.questionValue*o.value)
        #total=total/
        Attempt.objects.filter(id=attempt.id).update(score=total)'''
# Create your models here.
