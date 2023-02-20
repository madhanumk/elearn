from django.contrib import admin
from .models import Quiz, Question,Option, Assignment, Response, Attempt
from django_summernote.admin import SummernoteModelAdmin, SummernoteWidget
from django.db import models
from general.models import Subject_Assignment,Student
from django.db.models import Avg,Sum
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.filters import RelatedFieldListFilter
# Register your models here.

'''
class Gradefilter(SimpleListFilter):  
  title = ('Grade')
  parameter_name = 'grade'

  def lookups(self, request, model_admin):    
    qs_grade = Grade.objects.all()
    list_grade = []
    for grade in qs_grade:
        list_grade.append(
            (grade.grade, grade.grade)
        )
    return (
        sorted(list_grade, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


class SubjectFilter(SimpleListFilter):  
  title = ('Subject Title')
  parameter_name = 'subject'

  def lookups(self, request, model_admin):    
    grade=request.GET.get('grade', None)
    group=request.GET.get('group', None)
    if request.user.is_superuser:
        qs_subject=Subject_Assignment.objects.filter()
    
    elif request.user.groups.filter(name='School').exists():
        qs_subject=[]
        if grade:
            if group:
                qs_subject=Subject_Assignment.objects.filter(group=group,grade__grade=grade,board=request.user.school.board).order_by('subject__subject_title')

            #qs_subject=Subject_Assignment.objects.filter(grade__grade=grade,board=request.user.school.board).order_by('subject__subject_title')
           
    elif request.user.groups.filter(name='Teacher').exists():
        qs_subject=[]
        subjectsd=Teacher.objects.filter(user=request.user).values('subjects')
        board=Teacher.objects.filter(user=request.user).values('subjects__board').distinct()
        
        if grade:
            if group:
                qs_subject=Subject_Assignment.objects.filter(group=group,id__in=subjectsd,grade__grade=grade,board__in=board).order_by('subject__subject_title')
            #qs_subject=Subject_Assignment.objects.filter(id__in=subjectsd,grade__grade=grade,board__in=board).order_by('subject__subject_title')
             


    list_subjects = []
    for subjects in qs_subject:
        list_subjects.append(
            (subjects.subject.id, subjects.subject.subject_title)
        )
    return (
        sorted(list_subjects, key=lambda tp:tp[1])
    )  

  def queryset(self, request, queryset):
      return queryset
'''


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    formfield_overrides = {models.TextField: {'widget': SummernoteWidget}}


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        question=request.GET.get('name', None)
        if not question:
            question='hi'
        
        if db_field.name == "Question":
            if request.user.is_superuser:
                kwargs["queryset"] = Question.objects.all()
            elif request.user.groups.filter(name='School').exists():
                kwargs["queryset"] = Question.objects.filter(school=request.user.school)
           
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    date_hierarchy = 'openDate'
    list_display = ('name','openDate','closeDate')
    #list_filter = (Gradefilter,SubjectFilter)
    search_fields= ['name']
    inlines = [AssignmentInline]
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.college.category = request.user.college.category
        super().save_model(request, obj, form, change)

    '''def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("school", )
        form = super(QuizAdmin, self).get_form(request, obj, **kwargs)
        return form'''

    def get_queryset(self, request):
          #grade=request.GET.get('grade', None)
          subject=request.GET.get('subject', None)          
          if request.user.is_superuser:
              return Quiz.objects.all()
          elif request.user.groups.filter(name='School').exists():
              if grade:
                  if subject:
                      return Quiz.objects.filter(subjects__subject=subject,subjects__grade__grade=grade,school=request.user.school)
                  else:
                      return Quiz.objects.filter(subjects__grade__grade=grade,school=request.user.school)    
     
              else:
                  return Quiz.objects.filter(school=request.user.school)    

              

          

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "subjects":
            if request.user.is_superuser:
                kwargs["queryset"] = Subject_Assignment.objects.all()
            elif request.user.groups.filter(name='School').exists():
                kwargs["queryset"] = Subject_Assignment.objects.filter(board=request.user.school.board)   
            
        return super(QuizAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
        

    

#class SummernoteInlineModelAdmin(admin.options.InlineModelAdmin):
class OptionInline(admin.TabularInline):
    model = Option
    extra = 0
    formfield_overrides = {models.TextField: {'widget': SummernoteWidget}}



class QuestionModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    model = Question
    inlines = [OptionInline,AssignmentInline]
    formfield_overrides = {models.TextField: {'widget': SummernoteWidget}}
    list_display = ('name','description')
    #list_filter = (Gradefilter,SubjectFilter)
    search_fields= ['name','description']

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.school = request.user.school
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("school", )
        form = super(QuestionModelAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_queryset(self, request):
          subject=request.GET.get('subject', None) 
          
          if request.user.is_superuser:
              return Question.objects.all()
          elif request.user.groups.filter(name='School').exists():
              if subject:
                  return Question.objects.filter(subject=subject,school=request.user.school)
              else:
                  return Question.objects.filter(school=request.user.school)    
              

          

'''class OptionModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    formfield_overrides = {models.TextField: {'widget': SummernoteWidget}}
    def get_form(self, request, obj=None, **kwargs):
        
        form = super(OptionModelAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['Question'].queryset = Question.objects.filter(school=request.user.school)
        return form'''
    
'''@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('user_name','quiz_name','score')
    list_filter = ('Quiz__name','user__student__school__school_name','user__student__school__school_at__district_name')
    def get_queryset(self, request):
          attemptfilter = super(AttemptAdmin, self).get_queryset(request)
          if request.user.is_superuser:
              return attemptfilter
          return attemptfilter.filter(Quiz__school=request.user.school)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('Quiz','Question','marks')
    list_filter = ('Quiz__name','Question__name')
    def get_form(self, request, obj=None, **kwargs):
        self.fields = ('Quiz','Question','marks')
        form = super(AssignmentAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['Quiz'].queryset= Quiz.objects.filter(school=request.user.school)
            form.base_fields['Question'].queryset = Question.objects.filter(school=request.user.school)
        return form

    def get_queryset(self, request):
          assignfilter = super(AssignmentAdmin, self).get_queryset(request)
          if request.user.is_superuser:
              return assignfilter
          return assignfilter.filter(Quiz__school=request.user.school)

'''

class Studentfilter(SimpleListFilter):  
  title = ('Student')
  parameter_name = 'student'

  def lookups(self, request, model_admin):    
    grade=request.GET.get('grade', None)
    group=request.GET.get('group', None)
    get_board=request.GET.get('board', None)


    if request.user.groups.filter(name='School').exists():            
              board=request.user.school.board  
              school=request.user.school

    elif request.user.groups.filter(name='Teacher').exists(): 
              board=Teacher.objects.filter(user=request.user).values('subjects__board__board').distinct()
              board=board[0]['subjects__board__board']
              school=request.user.teacher.school
        

     
    if grade:
        if group:
            qs_stud = Student.objects.filter(board__board=board,grade__grade=grade,group=group,school=school)
        else:
            qs_stud = Student.objects.filter(board__board=board,grade__grade=grade,school=school)        
           
    else:
        if group:
            qs_stud = Student.objects.filter(board__board=board,group=group,school=school)
        else:
            qs_stud = Student.objects.filter(board__board=board,school=school)


    list_students = []
    for stud in qs_stud:
        list_students.append(
            (stud.user_id, stud.user.first_name)
        )
    return (
        sorted(list_students, key=lambda tp:tp[1])
    )  

  def queryset(self, request, queryset):
      return queryset




class Groupfilter(SimpleListFilter):  
  title = ('Group')
  parameter_name = 'group'

  def lookups(self, request, model_admin):
    grade=request.GET.get('grade', None)
    if grade=='XI' or grade=='XII':
        qs_group = Group.objects.exclude(group_name='General')
    else:
        qs_group=Group.objects.filter(group_name='General')
    list_group = []
    for group in qs_group:
        list_group.append(
            (group.id, group.group_name)
        )
    return (
        sorted(list_group, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
     return queryset






@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('user_name','quiz_name','score')
    #list_filter = (Gradefilter,Groupfilter,Studentfilter)
    #change_list_template = 'change_list_attempt.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        studentid=request.GET.get('student', None)
        grade=request.GET.get('grade', None)
        group=request.GET.get('group', None)
        
        

        
        data = dict()
        score=[]
        title=[]
        if request.user.is_superuser:
            self.list_filter = ()
            return super(AttemptAdmin, self).changelist_view(request, {})
        elif request.user.groups.filter(name='School').exists():
            self.list_filter = (Gradefilter,Groupfilter,Studentfilter,SubjectFilter)             
   
            if grade:
                if group:
                    if studentid:
                        sub_asign=list(Subject_Assignment.objects.filter(board__board=request.user.school.board,grade__grade=grade,group=group).values_list('id','subject__subject_title'))
                        for sub in sub_asign:
                            score.append(list(Attempt.objects.filter(user=studentid,user__student__grade__grade=grade,user__student__group=group,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                            title.append(sub[1]) 
                    else:
                        sub_asign=list(Subject_Assignment.objects.filter(board__board=request.user.school.board,grade__grade=grade,group=group).values_list('id','subject__subject_title'))
                        for sub in sub_asign:
                            score.append(list(Attempt.objects.filter(user__student__school=request.user.school,user__student__grade__grade=grade,user__student__group=group,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                            title.append(sub[1])
                   
                    
                else:
                    if studentid:
                        sub_asign=list(Subject_Assignment.objects.filter(board__board=request.user.school.board,grade__grade=grade).values_list('id','subject__subject_title'))    
                        for sub in sub_asign:
                            score.append(list(Attempt.objects.filter(user=studentid,user__student__school=request.user.school,user__student__grade__grade=grade,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                            title.append(sub[1])
                    else:
                        sub_asign=list(Subject_Assignment.objects.filter(board__board=request.user.school.board,grade__grade=grade).values_list('id','subject__subject_title'))    
                        for sub in sub_asign:
                            score.append(list(Attempt.objects.filter(user__student__school=request.user.school,user__student__grade__grade=grade,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                            title.append(sub[1])


            else:
                sub_asign=list(Subject_Assignment.objects.filter(board__board=request.user.school.board).values_list('id','subject__subject_title'))    
                
                for sub in sub_asign:
                    score.append(list(Attempt.objects.filter(user__student__school=request.user.school,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                    title.append(sub[1])

              
    

            score=[i[0] for i in score]
            score = [str(i or '0') for i in score] 
           
            
            return super(AttemptAdmin, self).changelist_view(request, {'extra_context': score,'subjects':title,})
        
        elif request.user.groups.filter(name='Teacher').exists():
            subject_id=request.GET.get('subject', None)
            self.list_filter = (Gradefilter,Groupfilter,SubjectFilter,Studentfilter)
            board=Teacher.objects.filter(user=request.user).values('subjects__board__board').distinct()
            board=board[0]['subjects__board__board']
            school=request.user.teacher.school
            subjects=Teacher.objects.filter(user=request.user).values('subjects')

            if grade:
                if group:
                    if subject_id:
                        
                        if studentid:
                            
                            sub_asign=list(Subject_Assignment.objects.filter(subject=subject_id,id__in=subjects,board__board=board,grade__grade=grade,group=group).values_list('id','subject__subject_title'))
                            for sub in sub_asign:
                                score.append(list(Attempt.objects.filter(user=studentid,user__student__grade__grade=grade,user__student__group=group,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                                title.append(sub[1]) 
                        else:
                            sub_asign=list(Subject_Assignment.objects.filter(subject=subject_id,id__in=subjects,board__board=board,grade__grade=grade,group=group).values_list('id','subject__subject_title'))
                            for sub in sub_asign:
                                score.append(list(Attempt.objects.filter(user__student__school=school,user__student__grade__grade=grade,user__student__group=group,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                                title.append(sub[1])
                    else:
                        if studentid:
                            
                            sub_asign=list(Subject_Assignment.objects.filter(id__in=subjects,board__board=board,grade__grade=grade,group=group).values_list('id','subject__subject_title'))
                            for sub in sub_asign:
                                score.append(list(Attempt.objects.filter(user=studentid,user__student__grade__grade=grade,user__student__group=group,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                                title.append(sub[1]) 
                        else:
                            sub_asign=list(Subject_Assignment.objects.filter(id__in=subjects,board__board=board,grade__grade=grade,group=group).values_list('id','subject__subject_title'))
                            for sub in sub_asign:
                                score.append(list(Attempt.objects.filter(user__student__school=school,user__student__grade__grade=grade,user__student__group=group,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                                title.append(sub[1])

                    
                else:
                    if studentid:
                        sub_asign=list(Subject_Assignment.objects.filter(id__in=subjects,board__board=board,grade__grade=grade).values_list('id','subject__subject_title'))    
                        for sub in sub_asign:
                            score.append(list(Attempt.objects.filter(user=studentid,user__student__school=school,user__student__grade__grade=grade,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                            title.append(sub[1])
                    else:
                        sub_asign=list(Subject_Assignment.objects.filter(id__in=subjects,board__board=board,grade__grade=grade).values_list('id','subject__subject_title'))    
                        for sub in sub_asign:
                            score.append(list(Attempt.objects.filter(user__student__school=school,user__student__grade__grade=grade,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                            title.append(sub[1])


            else:
                sub_asign=list(Subject_Assignment.objects.filter(id__in=subjects,board__board=board).values_list('id','subject__subject_title'))    
                
                for sub in sub_asign:
                    score.append(list(Attempt.objects.filter(user__student__school=school,Quiz__subjects=sub[0]).aggregate(Avg('score')).values()))
                    title.append(sub[1])

              
    

            score=[i[0] for i in score]
            score = [str(i or '0') for i in score] 
           
            
            return super(AttemptAdmin, self).changelist_view(request, {'extra_context': score,'subjects':title,})





    def get_queryset(self, request):
    
          
          if request.user.is_superuser:              
              return Attempt.objects.all()

          elif request.user.groups.filter(name='School').exists():
              studentid=request.GET.get('student', None)
              grade=request.GET.get('grade', None)
              group=request.GET.get('group', None)


              if grade:
                  if group:
                      if studentid:
                          return Attempt.objects.filter(user=studentid,user__student__group=group,user__student__grade__grade=grade,user__student__school=request.user.school,user__student__board__board=request.user.school.board)
                      else:
                          return Attempt.objects.filter(user__student__group=group,user__student__grade__grade=grade,user__student__school=request.user.school,user__student__board__board=request.user.school.board)    
                      
                  else:
                      if studentid:
                          return Attempt.objects.filter(user=studentid,user__student__grade__grade=grade,user__student__school=request.user.school,user__student__board__board=request.user.school.board)    
                      else:
                          return Attempt.objects.filter(user__student__grade__grade=grade,user__student__school=request.user.school,user__student__board__board=request.user.school.board)        
                      
                  
              else:
                  if group:
                      if studentid:
                          return Attempt.objects.filter(user=studentid,user__student__group=group,user__student__school=request.user.school,user__student__board__board=request.user.school.board) 
                      else:
                          return Attempt.objects.filter(user__student__group=group,user__student__school=request.user.school,user__student__board__board=request.user.school.board)     
                      
                  else:
                      if studentid:
                          return Attempt.objects.filter(user=studentid,user__student__school=request.user.school,user__student__board__board=request.user.school.board)     
                      else:
                          return Attempt.objects.filter(user__student__school=request.user.school,user__student__board__board=request.user.school.board)         
          
          elif request.user.groups.filter(name='Teacher').exists(): 

              studentid=request.GET.get('student', None)
              grade=request.GET.get('grade', None)
              group=request.GET.get('group', None)
              subject_id=request.GET.get('subject', None)

              board=Teacher.objects.filter(user=request.user).values('subjects__board__board').distinct()
              board=board[0]['subjects__board__board']
              school=request.user.teacher.school
              subjects=Teacher.objects.filter(user=request.user).values('subjects')


              if grade:
                  if group:
                      if subject_id:
                          if studentid:
                              return Attempt.objects.filter(Quiz__subjects__subject=subject_id,Quiz__subjects__in=subjects,user=studentid,user__student__group=group,user__student__grade__grade=grade,user__student__school=school,user__student__board__board=board)
                          else:
                              return Attempt.objects.filter(Quiz__subjects__subject=subject_id,Quiz__subjects__in=subjects,user__student__group=group,user__student__grade__grade=grade,user__student__school=school,user__student__board__board=board)    
                      else:

                          if studentid:
                              return Attempt.objects.filter(Quiz__subjects__subject=subject_id,Quiz__subjects__in=subjects,user=studentid,user__student__group=group,user__student__grade__grade=grade,user__student__school=school,user__student__board__board=board)
                          else:
                              return Attempt.objects.filter(Quiz__subjects__subject=subject_id,Quiz__subjects__in=subjects,user__student__group=group,user__student__grade__grade=grade,user__student__school=school,user__student__board__board=board)    

                  else:
                      if studentid:
                          return Attempt.objects.filter(Quiz__subjects__in=subjects,user=studentid,user__student__grade__grade=grade,user__student__school=school,user__student__board__board=board)    
                      else:
                          return Attempt.objects.filter(Quiz__subjects__in=subjects,user__student__grade__grade=grade,user__student__school=school,user__student__board__board=board)        
                      
                  
              else:
                  if group:
                      if studentid:
                          return Attempt.objects.filter(Quiz__subjects__in=subjects,user=studentid,user__student__group=group,user__student__school=school,user__student__board__board=board) 
                      else:
                          return Attempt.objects.filter(Quiz__subjects__in=subjects,user__student__group=group,user__student__school=school,user__student__board__board=board)     
                      
                  else:
                      if studentid:
                          return Attempt.objects.filter(Quiz__subjects__in=subjects,user=studentid,user__student__school=school,user__student__board__board=board)     
                      else:
                          return Attempt.objects.filter(Quiz__subjects__in=subjects,user__student__school=school,user__student__board__board=board)         
                     

                     

              
               
              


admin.site.register(Question,QuestionModelAdmin)
#admin.site.register(Option,OptionModelAdmin)
#admin.site.register(Response)





