from django.contrib import admin
from django.contrib.admin import  SimpleListFilter
from general.models import Faculty
from .models import Log_Book, Log_Book_Entry
# Register your models here.

class Log_Book_Entry_Inline(admin.TabularInline):
    model = Log_Book_Entry


class Teacher_Filter(SimpleListFilter):
      
  title = ('teacher')
  parameter_name = 'teacher'

  def lookups(self, request, model_admin):  
    if request.user.is_superuser:
      qs_teachers = Faculty.objects.all()
    else:
      qs_teachers = Faculty.objects.filter(school=request.user.school)

    list_teacher = []
    for teacher in qs_teachers:
        list_teacher.append(
            (teacher.id, str(teacher))
        )
    return (
        sorted(list_teacher, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


@admin.register(Log_Book)
class LogBookAdmin(admin.ModelAdmin):
    list_display = ('date','submitted_by','subject')
    inlines = [Log_Book_Entry_Inline,]
    list_filter = ['subject',Teacher_Filter,'date']


    def get_queryset(self, request):    
      teacher_id = request.GET.get('teacher', None)
      logbook = super(LogBookAdmin, self).get_queryset(request)
      if request.user.is_superuser:        
        return logbook
      elif request.user.groups.filter(name='School').exists():
        if teacher_id:
          return logbook.filter(subject__teacher__id=teacher_id,subject__teacher__school=request.user.school)
        else:
          return logbook.filter(subject__teacher__school=request.user.school)