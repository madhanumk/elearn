from virtual_class.models import Assignment, Submission
from django.template import Library
from datetime import date
from django import template
 
register = Library()
 
@register.filter(name='check_duedate')
def check_duedate(value,user):

    submission=Submission.objects.filter(assignment_id=value,student=user.student) 
    if submission:
        return "Attended"
    else:
         assignment = Assignment.objects.get(id=value)
         if assignment.due_date < date.today():
             return "Over Due"
         else:
             return "Pending"   

register = template.Library()

@register.simple_tag
def get_attempt_status(assignment_id, user):
    try:
        submission = Submission.objects.get(assignment_id=assignment_id,student=user.student)
        return submission
    except:
        return "Not Attended"
           
  
    
 
  