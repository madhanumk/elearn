# Signals that fires when a user logs in and logs out
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from . models import LoggedInUser
from general.models import Portal_Usage
from django.contrib.auth.models import User
import datetime
from datetime import timedelta


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
    user = User.objects.get(username=kwargs.get('user'))
    last_login = user.last_login
    try:
        if request.session['is_logout']:
            now = datetime.datetime.now()
        else:
            now =request.session['last_touch'] + timedelta(minutes=10)
    except KeyError:
        now = request.session['last_touch'] + timedelta(minutes=10)
    
    difference = (now - last_login).total_seconds() // 60.0
    session_obj, created = Portal_Usage.objects.get_or_create(user=kwargs.get('user'),date=datetime.date.today())
    if created:
        session_obj.mins = difference
    else:
        session_obj.mins += difference
    session_obj.save()


    
    
     