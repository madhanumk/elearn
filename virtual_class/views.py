import imp
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from general.models import Subject_Assignment,Chapter
from .models import ClassRoom,Upcoming_Session,Topic,Assignment,Material,Video,Submission,Forum,Reply
from datetime import date
from .forms import SubmissionForm,ForumForm,ReplyForm
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
# Create your views here.

@login_required(login_url='login')
def virtualclass(request):
    if request.user.groups.filter(name='faculty').exists():
        return redirect('/faculty')
        
    elif  request.user.groups.filter(name='Student').exists():
        stud = request.user.student
        croom=ClassRoom.objects.filter(subject_assignment__programme=stud.programme,subject_assignment__year=stud.year,subject_assignment__semester=stud.semester,activate=True)
        chapter = Chapter.objects.filter(subject_assignment__programme=stud.programme,subject_assignment__year=stud.year,subject_assignment__semester=stud.semester)  
        upcoming_session=Upcoming_Session.objects.filter(start_date__gte=date.today(),classroom__in=croom)
        return render(request, 'vt_class/virtualclass.html', {'crooms':croom,'upcoming_session':upcoming_session,'chapter':chapter})

@login_required(login_url='login')       
def classroom_subject(request,id):
    data =dict()
    classroom_id = id
    stud = request.user.student
    subject_assignment = ClassRoom.objects.filter(id=id).values_list('subject_assignment',flat=True).distinct()
    print("subject_assignment",subject_assignment)
    chapter = Chapter.objects.filter(subject_assignment__in=subject_assignment)
    print("chapters",chapter)
    return render(request,'vt_class/chapter_details.html',{'chapter':chapter,'id':id})
    #data['chapters'] = render_to_string('vt_class/chapter_details.html', {'chapter':chapter,'id':id},request)
    #data['chapter_id'] = id
    #return JsonResponse(data)  


@login_required(login_url='login')
def topic_view(request,pk):
    chapter = Chapter.objects.get(id=pk)
    stud = request.user.student
    topic = Topic.objects.filter(chapter=pk,chapter__subject_assignment__programme=stud.programme).order_by('created_on')
    assignment=Assignment.objects.filter(topic__in=topic).order_by('due_date')
        
    return render(request, 'vt_class/view_topic.html', {'topics':topic,'assignment':assignment,'chapter':chapter,})

@login_required(login_url='login')
def topic_resources(request,pk):
    stud = request.user.student 
    topic = Topic.objects.get(id=pk)   
    materials = Material.objects.filter(topic=pk,topic__chapter__subject_assignment__programme=stud.programme).order_by('added_on')
    videos = Video.objects.filter(topic=pk,topic__chapter__subject_assignment__programme=stud.programme).order_by('added_on')
    return render(request, 'vt_class/view_material.html', {'materials':materials,'videos':videos,'topic':topic,})

@login_required(login_url='login')
def assignment_view(request,pk,):
    if request.method == 'POST':    
        form = SubmissionForm(request.POST,  request.FILES) 
        submission=Submission.objects.filter(assignment_id=pk,student=request.user.student)
        if not submission:
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment_id=pk
                submission.student=request.user.student
                submission.marks=0
                submission.status='S'
                submission = form.save()
               
            
            return redirect('topic',pk=submission.assignment.topic.chapter.id)
        else:
            return redirect('/vtclass/')

 
    else:        
        if Submission.objects.filter(assignment_id=pk,student=request.user.student):            
            assignment=None
        else:
            stud=request.user.student
            assignment=Assignment.objects.get(id=pk,topic__chapter__subject_assignment__programme=stud.programme)
        print(assignment)
        form = SubmissionForm()
        return render(request, 'vt_class/view_assignment.html', {'assignment':assignment,'form':form}) 

@login_required(login_url='login')
def delete_submission(request,pk):
    data=dict()
    stud = request.user.student
    submission=Submission.objects.get(id=pk,student=stud)
    if submission.student == stud:
        submission.delete()        
        data['status'] = True
        page=request.GET.get('page', None)
        if page == "home":
            assignments = Assignment.objects.filter(topic__croom__subject_assignment__programme=stud.programme,topic__croom__activate=True).order_by('due_date')
            data['html'] =  render_to_string('vt_class/assignment_list.html',{'assignments':assignments,},request)  
    else:
        data['status'] = False
    
    return JsonResponse(data)


@login_required(login_url='login')
def ask_questions(request,pk,):

    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.topic_id=pk
            forum.created_by=request.user
            forum = form.save()
            
            return redirect('view_discussion',pk=pk)
 
    else:
        stud=request.user.student        
        topic = Topic.objects.get(id=pk,chapter__subject_assignment__programme=stud.programme)
        form= ForumForm()
        return render(request, 'vt_class/ask_questions.html', {'form':form,'topic':topic}) 
      
        
@login_required(login_url='login')
def view_discussion(request,pk):
    stud=request.user.student
    
    topic=Topic.objects.get(id=pk,chapter__subject_assignment__programme=stud.programme)
    return render(request, 'vt_class/view_discussion.html', {'topic':topic,}) 
    
       
@login_required(login_url='login')
def view_replies(request,pk):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)  
            reply.forum_id=pk
            reply.posted_by=request.user
            reply=form.save()          

            return redirect('view_replies', pk=pk)
 
    else:
        stud=request.user.student
        forum=Forum.objects.get(id=pk,topic__chapter__subject_assignment__programme=stud.programme)       
        reply=Reply.objects.filter(forum=forum)     
        form=ReplyForm()
        return render(request, 'vt_class/view_replies.html', {'reply':reply,'forum':forum,'form':form,})  
       
        
@login_required(login_url='login')
def ajax_topic_assign(request):
    data=dict()
    title=request.GET.get('title') 
    classroom=ClassRoom.objects.get(id=request.GET.get('object_id'))
    Topic.objects.create(croom=classroom,title=title)
    data['status'] = "Done"       

    return JsonResponse(data)

#@csrf_exempt
@login_required(login_url='login')
def ajax_material_assign(request):
    data=dict()   
    title=request.POST.get('title')  

    material_file=request.FILES.getlist('file')   
    file_object = material_file[0]
    topic=Topic.objects.get(id=request.POST.get('object_id'))   

    Material.objects.create(topic=topic,title=title,material=material_file[0])
    data['status'] = "Done"       

    return JsonResponse(data)


@login_required(login_url='login')
def ajax_video_assign(request):
    data=dict()
    title=request.GET.get('title')
    link=request.GET.get('link')
    topic=Topic.objects.get(id=request.GET.get('object_id'))
    Video.objects.create(topic=topic,title=title,link=link)
    data['status'] = "Done"       

    return JsonResponse(data)

@login_required
def draw_chart(request):
    data = dict()
    stud = request.user.student
    subjects = list(Subject_Assignment.objects.filter(programme=stud.programme,year=stud.year,semester=stud.semester).values_list('id','subject__subject_title').order_by('subject__subject_title'))
    sub_title = list()
    sub_assign = list()
    scores = list()
    for sub in subjects:
        sub_title.append(sub[1])
        sub_assign.append(sub[0])
    print("subjects_assignments",sub_title)
    data['subjects'] = sub_title
    for sub in sub_assign:
        scores.append(list(Submission.objects.filter(status="A",student=stud,assignment__topic__croom__subject_assignment__in=(sub,)).values_list('marks',flat=True)))
    print("subjects_assignmnets_scores",scores)
    data['scores'] = scores

    return JsonResponse(data) 