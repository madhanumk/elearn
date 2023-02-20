from django.db import models

# Create your models here.
from general.models import Faculty_Subject_Assignment


# Create your models here.

hour_options = (('','Choose hour'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'))


class Log_Book(models.Model):
    date = models.DateField(auto_now_add=True)
    subject = models.ForeignKey(Faculty_Subject_Assignment,on_delete=models.CASCADE) 
    is_day_update = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.date)

    def submitted_by(self):
        return self.subject.teacher

    class Meta:
        verbose_name_plural = 'Log Book'
        
class Log_Book_Entry(models.Model):
    log_book = models.ForeignKey(Log_Book, on_delete=models.CASCADE)
    hour = models.CharField(choices=hour_options,max_length=1)
    chapter = models.CharField(max_length=300)
    content_delivered = models.TextField(max_length=300)
    activity = models.TextField(max_length=300)

    class Meta:
        ordering = ('hour',)