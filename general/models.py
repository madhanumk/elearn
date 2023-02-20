from statistics import mode
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

#Global Variable 
gender_options=(('','Choose Gender'),('M','Male'),('F','Female'),('T','Transgender'))
graduation_code=(('','Choose Graduation'),('UG','Under Graduate'),('PG','Post Graduate'),('Phd','Phd'))
year=(('','Choose Year'),('1','I - Year'),('2','II - Year'),('3','III - Year'),('4','IV - Year'),('5','V - Year'))
semester=(('','Choose Semester'),('1','I - Semester'),('2','II - Semester'),('3','III - Semester'),('4','IV - Semester'),('5','V - Semester'),('6','VI - Semester'),('7','VII - Semester'),('8','VIII - Semester'))
section_options = (('','Choose Section'),('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),('H','H'))

class Portal_Usage(models.Model):
    user = models.ForeignKey(User, related_name='logged_in_user_1',on_delete=models.CASCADE)
    date = models.DateField()
    mins = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username

    def username(self):
        return self.user.first_name + ' ' + self.user.last_name

class Meta:
        verbose_name = 'Portal Usage'
        verbose_name_plural = 'Portal Usage'


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "-"+ self.country.name 

class District(models.Model):
    name = models.CharField(max_length=20)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + "-"+ self.state.name 

class Degree_Categaroy(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class Graduation(models.Model):
    code = models.CharField(choices=graduation_code,max_length=3)
    description = models.TextField()

    def __str__(self):
        return self.code

class Department(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    degree_category = models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE)


    def __str__(self):
        return self.short_name + "-" + self.degree_category.category

class Programme(models.Model):
    title = models.CharField(max_length=100)
    department= models.ForeignKey(Department,on_delete=models.CASCADE)
    graduation = models.ForeignKey(Graduation,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + "-" + self.department.name + "-" + self.graduation.code

def current_year():
    return datetime.date.today().year+1

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value) 

class Acadmic_Year(models.Model):
    title = models.CharField(max_length=9)
    start_year = models.IntegerField(_('start year'), validators=[MinValueValidator(2008), max_value_current_year])
    end_year = models.IntegerField(_('End year'), validators=[MinValueValidator(2008), max_value_current_year])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class Subject_Category(models.Model):
    category_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Subject(models.Model):
    subject_title = models.CharField(max_length=50)
    course_code = models.CharField(max_length=30,blank=True)
    subject_category = models.ForeignKey(Subject_Category,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    degree_categaroy = models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE)
    def __str__(self):
        return self.course_code+'-'+self.subject_title


class Subject_Assignment(models.Model):
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    year = models.CharField(choices=year,max_length=2)
    semester = models.CharField(choices=semester,max_length=2)

    def __str__(self):
        return self.subject.course_code+'-'+self.subject.subject_title + "-" +str(self.programme)


    def course_code(self):
        return self.subject.course_code


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=15)
    year = models.CharField(choices=year,max_length=2)
    semester = models.CharField(choices=semester,max_length=5)
    dob = models.DateField(help_text="Date of Birth",null=True,blank=True) 
    gender = models.CharField(choices=gender_options,max_length=1)
    mobile_no = models.CharField(max_length=10)
    address = models.TextField()
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    #degree_categaroy = models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE)
    #graduation = models.ForeignKey(Graduation,on_delete=models.CASCADE)
    #department = models.ForeignKey(Department,on_delete=models.CASCADE)
    section=models.CharField(choices=section_options,max_length=1,null=True,blank=True,default='A')
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE)
    dor = models.DateField(auto_now_add=True)
    acadmic_year = models.ForeignKey(Acadmic_Year,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name
        
        #Getter Methods

    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return  self.user.last_name

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10)
    gender = models.CharField(choices=gender_options,max_length=1,blank=True)
    address = models.TextField()
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    category = models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE)
    graduation = models.ForeignKey(Graduation,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE)
    dor = models.DateField(auto_now_add=True)
    subject_category = models.ForeignKey(Subject_Category,on_delete=models.CASCADE,null=True)
    acadmic_year = models.ForeignKey(Acadmic_Year,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user.first_name

class Recent(models.Model):
    pre_title = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    urlload=models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title  

class Learning_Style(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    learning_style = models.CharField(max_length=25)
    def __str__(self):
        return self.learning_style
    
class Faculty_Subject_Assignment(models.Model):
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    subject =  models.ForeignKey(Subject_Assignment,on_delete=models.CASCADE,related_name="subjects")
    section = models.CharField(choices=section_options,max_length=1,null=True)

    def __str__(self):
        return self.subject.subject.course_code+'-'+self.subject.subject.subject_title+'-'+str(self.section) 


class College(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    #school_name = models.CharField(max_length=100)
    #school_at = models.ForeignKey(District,on_delete=models.CASCADE)
    category=models.ForeignKey(Degree_Categaroy,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.first_name+"-"+str(self.category)
    
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return  self.user.last_name
    
class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject_assignment = models.ForeignKey(Subject_Assignment, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name+'-'+str(self.subject_assignment)