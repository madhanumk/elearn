from statistics import mode
from django.contrib import admin
from . import models
from .models import User,Student,Country,State,District,Degree_Categaroy,Department,Faculty,Subject_Category,Subject,Faculty_Subject_Assignment,Subject_Assignment, Chapter, Portal_Usage
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from virtual_class.models import Topic

#admin.site.unregister(User)
# Define the admin class

admin.site.unregister(User)#class UserAdmin(UserAdmin):
    #list_display: ('first_name')

class CustomUserAdmin(UserAdmin):
    list_display: ('first_name')

admin.site.register(User, CustomUserAdmin)



admin.site.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name')

# Define the admin class
admin.site.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name')

# Define the admin class
admin.site.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name')

# Define the admin class
admin.site.register(Degree_Categaroy)
class Degree_CategaroyAdmin(admin.ModelAdmin):
    list_display = ('category')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')

# Define the admin class
class StudentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'year', 'semester','dob','gender','mobile_no','address','district','pincode']
admin.site.register(Student, StudentAdmin)

#class StudentAdmin(admin.ModelAdmin):
    #list_display = ('roll_number','user', 'programme')


# Define the admin class
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user','department','programme', 'acadmic_year')

class Teacher_Subject_Inline(admin.TabularInline):
    model = Faculty_Subject_Assignment
    extra=0
    fk_name = "Faculty"

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(Teacher_Subject_Inline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'subject':    
          if request.user.groups.filter(name='College').exists():
            field.queryset = field.queryset.filter(board = request.user.college)
        
        return field





admin.site.register(models.Faculty_Subject_Assignment)
admin.site.register(models.Graduation)
admin.site.register(models.Programme)
admin.site.register(models.Acadmic_Year)


class SubjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['subject_title', 'course_code','subject_category']

class Portal_Usage_Admin(admin.ModelAdmin):
    list_display = ['user', 'mins','date']

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Portal_Usage,Portal_Usage_Admin)

class Subject_CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['category_name']
admin.site.register(Subject_Category,Subject_CategoryAdmin)



class Chapter_Inline(admin.TabularInline):
    model = Chapter





class Subject_AssignmentAdmin(admin.ModelAdmin):
    list_display = ['programme','subject','year','semester']
    inlines = [Chapter_Inline]


class Topic_Inline(admin.TabularInline):
    model = Topic


class Chapter_Admin(admin.ModelAdmin):
    list_display = ['name','subject_assignment']
    inlines = [Topic_Inline]

admin.site.register(Subject_Assignment,Subject_AssignmentAdmin)

admin.site.register(models.College)
admin.site.register(Chapter,Chapter_Admin)