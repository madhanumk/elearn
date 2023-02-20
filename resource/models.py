from tkinter import CASCADE
from django.db import models
from .slugify import unique_slug_generator
from django.dispatch import receiver
from django.contrib.auth.models import User
from general.models import Subject, Degree_Categaroy,Graduation,Subject_Assignment,Programme
from uuid import uuid4
from os import path as os_path
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
learning_style_options = (('','Choose Learning Style'),('V','Visual'),('A','Auditory'),('K','Kinaesthetic'))

#File Upload Location
def path_and_rename(instance, filename):
    upload_to = 'elearn'

    if type(instance) == type(Resource()):
        upload_to = 'books'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os_path.join(upload_to, filename)

# Create your models here.
class Post_Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

class Post(models.Model):
    post_title = models.CharField(max_length = 225)
    slug = models.SlugField(max_length=255,unique=True, null=True, blank=True)
    post_body = RichTextUploadingField()
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateField(null=True)
    post_category = models.ForeignKey(Post_Category,on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject_Assignment)
    graduation = models.ForeignKey(Graduation,on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE,null=True)
    degree_categaroy = models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.post_title
    
#File Validator for File upload
def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'File should be in PDF Format')   
    
class Resource(models.Model):
    resource_name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50,null=True)
    publication = models.CharField(max_length=100,null=True)
    resource_file = models.FileField(upload_to=path_and_rename,null=True,blank=True,validators=[validate_file_extension])
    resource_link = models.CharField(max_length=200, null=True,blank=True)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    #subject = models.ManyToManyField(Subject_Assignment,related_name='re_subject')
    #graduation = models.ForeignKey(Graduation,on_delete=models.CASCADE)
    #programme = models.ManyToManyField(Programme)
    term_no = models.CharField(max_length=10,null=True)
    subject_assignment = models.ManyToManyField(Subject_Assignment)
    is_active = models.BooleanField(default=True)
  
    def __str__(self):
        return self.resource_name

class Video(models.Model):
    video_title = models.CharField(max_length=100)
    video_link = models.CharField(max_length=100)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    chapter_no = models.IntegerField()
    learning_style =models.CharField(choices=learning_style_options,max_length=1,default="V")
    
    def __str__(self):
        return self.video_title

    def resource_name(self):
        return self.resource.resource_name
    
    def author_name(self):
        return self.resource.author_name
    
    def publication(self):
        return self.resource.publication

class college_Resource_Map(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    Degree_Categaroy = models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.resource.resource_name
    
    #Getter Methods

    def resource_name(self):
        return self.resource.resource_name
    
    def author_name(self):
        return self.resource.author_name
    
    def publication(self):
        return self.resource.publication
    
    def school_name(self):
        return  self.school.school_name
    
#To Create Slug
@receiver(models.signals.pre_save, sender=Post)
def auto_slug_generator(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
