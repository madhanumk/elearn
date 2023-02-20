from django.forms import ModelForm
from .models import Quiz,Response

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        labels = {
            'name':'Quiz Name',
            'type':'Quiz Type',
            'openDate':'Quiz Start Date',
            'closeDate':'Quiz Close Date',
        }

class ResponseForm(ModelForm):
    class Meta:
        model= Response
        fields='__all__'