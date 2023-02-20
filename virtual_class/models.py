from io import open_code
from django.db import models
from quiz.models import On_Test
from general.models import Subject_Assignment,User,Student,Chapter,Faculty_Subject_Assignment
from uuid import uuid4
from os import path as os_path
from datetime import datetime, date
# Create your models here.
status_options = (('R','Requested'),('A','Accepted'),('D','Rejected'))
submission_options = (('S','Submitted'),('R','Resend'),('A','Accepted'))
visible_options = (('A','Student & Teacher'),('S','Student'))
 
#Materials upload path
def path_and_rename(instance, filename):  
    upload_to = instance.topic  

    if type(instance) == type(Material()):      
        croom_id=Topic.objects.filter(id=instance.topic.id).values_list('chapter',flat=True)
        classroom=ClassRoom.objects.filter(id__in=croom_id).first()     
        upload_to = str(classroom)
        topic = str(instance.topic)
        folder='materials'                 
        
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    return os_path.join(upload_to ,topic,folder, filename)



#afile upload path
def afile_path_and_rename(instance, filename):    
    upload_to = instance.title
    if type(instance) == type(Assignment()):       
        classroom_id = []
        topic_name = []           
        topic_name.append(instance.topic.title)
        t_name=topic_name
        t_name=''.join(t_name) 
 
        upload_to = str(instance.topic.chapter)
        topic=str(t_name)
        assignment_name=str(instance.title)
        folder='afile'

        
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    return os_path.join(upload_to ,topic,assignment_name,folder, filename)
    
#sfile upload path
def sfile_path_and_rename(instance, filename):   
  
    upload_to = instance.assignment.title
    if type(instance) == type(Submission()):
 
        t_name=str(instance.assignment.topic)
        t_name=''.join(t_name) 
        assignment_title=str(instance.assignment)
        assignment_title=''.join(assignment_title)             
        upload_to = str(instance.assignment.topic)
        topic=str(t_name)
        assignment_name=str(assignment_title)
        folder='sfile'        
                 
        
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    return os_path.join(upload_to ,topic ,assignment_name, folder, filename)

     



class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    subject_assignment = models.ForeignKey(Subject_Assignment,on_delete=models.CASCADE,null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    activate = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=50)
    #croom = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    faculty_subject_assignment = models.ForeignKey(Faculty_Subject_Assignment, on_delete=models.CASCADE,null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title + ' (' + str(self.chapter) + ')'
    def chaptername(self):
        return self.chapter.name
'''
    def changeform_link(self):
        if self.id:x
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
            'admin:vt_class_topic_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Topic</a>' % changeform_url)
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''  


     '''

class Material(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    material = models.FileField(upload_to=path_and_rename)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title 

    @property
    def material_url(self):
        if self.material:
            return self.material.url 

               

class Video(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    link =  models.CharField(max_length=255,verbose_name="Video Link")
    added_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Assignment(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    posted_on = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    marks = models.IntegerField()
    afile = models.FileField(upload_to="assignment",null=True,verbose_name='Assignment File')

    def __str__(self):
        return self.title


    def classroom(self):
        return self.topic.chapter

    @property
    def strength(self):
        print(self.topic.chapter.subject_assignment)
        subject_assignment=self.topic.chapter.subject_assignment
        #for subject_assignment in self.topic.croom.subject_assignment.all():
        year= subject_assignment.year
        semester=subject_assignment.semester
        count = Student.objects.filter(programme=self.topic.chapter.subject_assignment.programme,year=year,semester=semester).count()
        return count

    @property
    def submitted_count(self):
        count = Submission.objects.filter(assignment__id=self.id).count()
        return count

    @property
    def afile_url(self):
        if self.afile:
            return self.afile.url 

    @property
    def date_comparing(self):
        if self.due_date >= date.today():            
            return True
        else:
            return False 

class Submission(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True) 
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    subject_assignment = models.ManyToManyField(Subject_Assignment)  
    submitted_on = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField()
    status = models.CharField(choices=submission_options,max_length=1)
    sfile = models.FileField(upload_to="submission",null=True,verbose_name="Submission File")
    corrected_answer_sheet=models.FileField(upload_to='corrected_answer_sheet',blank=True,null=True)

    class Meta:
        ordering = ('-status',)
'''
    def sfile_download(self):
        return mark_safe('<a href="/media/{0}" download>{1}</a>'.format(self.sfile, self.sfile))

    sfile_download.short_description = 'Download File'


    def __str__(self):
        return self.assignment.title

    def grade(self):
        return self.student.grade

    def group(self):
        return self.student.group

    def classroom(self):
        return self.assignment.topic.croom        


    def changeform_link(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
            'admin:vt_class_submission_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Submissions</a>' % changeform_url)
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''

'''
class Forum(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    visible_to =  models.CharField(choices=visible_options,max_length=1,default="A")
    def __str__(self):
        return self.title

class Reply(models.Model):
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)
    description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)



class Upcoming_Session(models.Model):
    classroom=models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    start_date=models.DateField(null=True)
    start_time = models.TimeField(null=True)
    link=models.URLField(max_length=200)
    password_if_any=models.CharField(max_length=30,blank=True,null=True)


    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Session'

    def __str__(self):
        return self.title
