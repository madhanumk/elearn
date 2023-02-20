from django import forms
from .models import Submission,Forum,Reply


class SubmissionForm(forms.ModelForm):
    sfile = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))  
    class Meta:
        model = Submission
        fields = ('sfile',)


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('title','description','visible_to')

     

class ReplyForm(forms.ModelForm):    
    class Meta:
        model = Reply
        fields = ('description',)                
            
    