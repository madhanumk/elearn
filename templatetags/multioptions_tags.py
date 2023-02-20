from quiz.models import Option
from django.template import Library
 
register = Library()
 
@register.filter(name='checkmultioption')
def checkmultioption(value):
   count = Option.objects.filter(Question_id=value,value__gt=0.0).count()
   if count > 1:
      return True
   else:
      return False


@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 