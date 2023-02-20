from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.ClassRoom)
admin.site.register(models.Assignment)
admin.site.register(models.Topic)
admin.site.register(models.Forum)
admin.site.register(models.Submission)