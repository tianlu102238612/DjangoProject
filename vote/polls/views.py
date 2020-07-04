from django.shortcuts import render,redirect
from polls.models import Subject,Teacher
from django.http import JsonResponse
from django.http import HttpResponse,HttpRequest

def show_subjects(request):
    subjects = Subject.objects.all().order_by('no')
    return render(request, 'subjects.html', {'subjects':subjects})

def show_teachers(request):
    try:
        sno = int(request.GET.get('sno'))
        teachers = []
        if sno:
            subject = Subject.objects.only('name').get(no=sno)
            teachers = Teacher.objects.filter(subject=subject).order_by('no')
        return render(request,'teachers.html',{
            'subject':subject,
            'teachers':teachers
            })
    except (ValueError, Subject.DoesNotExist):
        return redirect('/')
    
def good_or_bad(request):
    try:
        tno = int(request.GET.get('tno'))
        teacher = Teacher.objects.get(no=tno)
        if request.path.startswith('/good'):
            teacher.good_count += 1
            count = teacher.good_count
        else:
            teacher.bad_count += 1
            count = teacher.bad_count
        print(count)
        teacher.save()
        data = {'code':20000,'mesg':'vote success','count':count}
    except (ValueError,Teacher.DoesNotExist):
        data = {'code':20001,'mesg':'vote fail'}

    return JsonResponse(data)

def login(request: HttpRequest) -> HttpResponse:
    hint = ''
    return render(request, 'login.html', {'hint': hint})
        
            
    
