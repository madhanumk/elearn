from django import forms
from django.contrib.auth.models import User
from general.models import Student, Faculty, Subject_Assignment,Programme
from resource.models import Post, Video
from ckeditor.fields import RichTextField


class StudentEditForm(forms.ModelForm):
   
    dob=forms.DateField(widget=forms.TextInput(attrs={'type': 'date','placeholder':'DOB'} ) )  
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'cols':25,'placeholder':'Address'}))
    mobile_no = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'} ))
    pincode = forms.CharField(max_length=6,widget=forms.TextInput(attrs={'placeholder':'PinCode'} ))
    class Meta:
        model = Student
        fields = ('dob', 'gender', 'address', 'mobile_no', 'district','pincode', 'programme', 'year', 'semester', 'acadmic_year')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['mobile_no'].widget.attrs['class'] = 'form-control'
        self.fields['district'].widget.attrs['class'] = 'form-control'
        self.fields['pincode'].widget.attrs['class'] = 'form-control'
        self.fields['programme'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'
        self.fields['semester'].widget.attrs['class'] = 'form-control'
        self.fields['acadmic_year'].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class TeacherEditForm(forms.ModelForm):   
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'cols':25,'placeholder':'Address'}))
    mobile_no = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'} ))
    pincode = forms.CharField(max_length=6,widget=forms.TextInput(attrs={'placeholder':'PinCode'} ))
    class Meta:
        model = Faculty
        fields = ('mobile_no', 'address','district','pincode',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile_no'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['district'].widget.attrs['class'] = 'form-control'
        self.fields['pincode'].widget.attrs['class'] = 'form-control'


class PostForm(forms.ModelForm):
    post_body=RichTextField()
    expires_on = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ) )  
    class Meta:
        model = Post
        fields = ['post_title','slug','post_body','expires_on','post_category','subjects','graduation','programme']
  
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['post_title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['post_body'].widget.attrs['cols'] = '100'
        self.fields['expires_on'].widget.attrs['class'] = 'form-control'
        self.fields['post_category'].widget.attrs['class'] = 'form-control'
        #self.fields['subjects'].widget.attrs['class'] = 'form-control'
        self.fields['graduation'].widget.attrs['class'] = 'form-control'
        #self.fields['programme'].widget.attrs['class'] = 'form-control'     
        #self.fields['degree_categaroy'].widget.attrs['class'] = 'form-control'
        self.fields['subjects'].queryset = Subject_Assignment.objects.filter(programme__department__degree_category=self.request.user.college.category)
        self.fields['programme'].queryset = Programme.objects.filter(department__degree_category=self.request.user.college.category) 

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_title','video_link','chapter_no','learning_style',]
  
      
