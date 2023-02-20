from django.template import Library

from quiz.models import Response,Option



register = Library()

@register.filter(name='check_answer')
def check_answer(value,user):

    try:       
        answer=Response.objects.filter(Assignment=value,user=user).values('Option__name')
        if len(answer):
            return answer[0]['Option__name']
        else:
            return None    
               
    except Response.DoesNotExist:
        return "Not Answered"