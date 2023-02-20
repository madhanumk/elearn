import imp
from django.shortcuts import render
from .models import Post,Resource
from django.contrib.auth.decorators import login_required, user_passes_test
from general.views import is_student, is_stud_faculty_user
from general.models import Subject_Assignment, Recent,Faculty,Learning_Style
from .models import Post, Video, Resource  
from django.http import HttpResponse, JsonResponse 
from django.template.loader import render_to_string
from re import match
import requests
from json import loads
# Create your views here.

def resource_view(request,pk):
    resource = Resource.objects.get(id=pk)
    file_path = resource.resource_file
    file_link = resource.resource_link
    '''  
    if request.user.groups.filter(name='student').exists():
        language = request.user.student.native_language
    elif request.user.groups.filter(name='Faculty').exists():
        language = request.user.teacher.native_language
    '''
    #delete duplicate record
    duplicate_obj = Recent.objects.filter(urlload=request.get_full_path(),user=request.user).delete()
     
    # if count is 5 delete last record
    if Recent.objects.filter(user=request.user).count()>4:
        last_recent=Recent.objects.filter(user=request.user).order_by('-date').last()
        last_recent.delete()

    R=Recent(pre_title='Book',title=resource.resource_name,urlload=request.get_full_path(),user=request.user)
    R.save()
    resource_term = Resource.objects.filter(resource_name=resource.resource_name)
    return render(request, 'resource/view_pdf.html', {'file_path':file_path,'file_link':file_link,'resource_terms':resource_term,'resource':resource})

    
def videos(request,pk):    
    videos = Video.objects.filter(resource=pk).order_by('chapter_no')
    return render(request,'video.html',{'videos':videos,})

def post_view(request,pk):
    try:
        if request.user.groups.filter(name='Student').exists():
            #posts = Post.objects.filter(programme=request.user.student.student.programme).exclude(Q(expires_on__lt=date.today()) | Q(slug=pk)).distinct().order_by('posted_on')
            posts = Post.objects.filter(programme=request.user.student.programme)
        '''elif  request.user.groups.filter(name='Teacher').exists():            
            subjects =Teacher.objects.filter(user=request.user).values_list('subjects',flat=True)
            posts = Post.objects.filter(subjects__in=subjects).exclude(Q(expires_on__lt=date.today()) | Q(slug=pk)).distinct().order_by('posted_on')   
        '''
        post = Post.objects.get(slug=pk)
        return render(request, 'resource/post.html', {'post':post,'posts':posts})
    except:
        post = Post.objects.get(slug=pk)
        posts = []
        print(posts)
        return render(request, 'resource/post.html', {'post':post,'posts':posts})
    
@login_required(login_url='login') #Authentication
@user_passes_test(is_stud_faculty_user,login_url='login')#Authorization
def video_filter(request,pk,style):
    data = dict()
    videos = Video.objects.filter(resource=pk,learning_style=style).order_by('chapter_no')
    data['html'] = render_to_string('resource/video_list.html',{'videos':videos},request)
    return JsonResponse(data)

#Ajax call View to get translation and Meaning
@login_required(login_url='login') #Authentication
@user_passes_test(is_stud_faculty_user,login_url='login')#Authorization
def fetch_translation(request):
    
    data=dict()
    word = request.GET.get('word')
    word = word.strip()
    source_str = word + "**"

    text = word
       
    if match("^[a-zA-Z0-9_ ]*$", word):      
        app_id  = "6cb497ec"
        app_key  = "dd"
        url = "https://od-api.oxforddictionaries.com/api/v2/entries/en/" + text
        meaning = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})

            
        
        if meaning.status_code == 200:
            meaning = loads(meaning.text)
            
            for counter in range(0,len(meaning['results'][0]['lexicalEntries'][0]['entries'][0]['senses'])):
                if 'definitions' in meaning['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][counter]:
                    source_str += "Definition:**" + meaning['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][counter]['definitions'][0] + "**.**"
                    
                if "examples" in meaning['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][counter]:
                    source_str += "Example:**" + meaning['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][counter]['examples'][0]['text'] + "**"
                source_str += " **"
                if counter == 2:
                    break

        else:
            
            url = "https://owlbot.info/api/v4/dictionary/"+text
            headers={'Content-Type': 'application/json','Authorization':'Token ' + 'dd' }
            meaning = requests.get(url,headers=headers)
            
                       
            if meaning.status_code == 200:
                meaning = loads(meaning.text)

                for definition in range(0,len(meaning['definitions'])):
                    source_str += "Definition:**" + meaning['definitions'][definition]['definition']+"**"
                    source_str += " **"
                    if definition == 2:
                        break
        language = "en"
        '''
        if request.user.groups.filter(name='student').exists():
            language = "en"
        elif request.user.groups.filter(name='Faculty').exists():
            language = "en"
        '''
        
        url = "https://translation.googleapis.com/language/translate/v2?key=ddddddddddddddd="+source_str+"&target="+str("en")
        translations = loads(requests.get(url).text)
        dest_str = translations['data']['translations'][0]['translatedText']

        english = source_str.split("**")
        tamil = dest_str.split("**")
        
        data['translation'] = tamil[0]
        data['english_mean'] = english
        data['tamil_mean'] = tamil
            
            
       
    return JsonResponse(data)