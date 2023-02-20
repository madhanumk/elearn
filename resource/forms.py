from django import forms
from resource.models import Resource, Video
from general.models import Subject_Assignment

class ResourceForm(forms.ModelForm):
    subject_assignment = forms.ModelMultipleChoiceField(queryset=Subject_Assignment.objects.all())
    class Meta:
        model = Resource
        fields = ['resource_name','author_name','publication','resource_file','resource_link','term_no','subject_assignment']
  