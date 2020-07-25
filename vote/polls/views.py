from django.shortcuts import render,redirect
from polls.models import Subject,Teacher,User
from django.http import JsonResponse
from django.http import HttpResponse,HttpRequest
from polls.utils import gen_md5_digest,Captcha,gen_random_code

from bpmappers import RawField
from bpmappers.djangomodel import ModelMapper
class SubjectMapper(ModelMapper):
    isHot = RawField('is_hot')
    class Meta:
        model = Subject
        exclude = ('create_date','is_hot')


def show_subjects(request):
    queryset = Subject.objects.all()
    subjects = []
    for subject in queryset:
        subjects.append(SubjectMapper(subject).as_dict())
    return JsonResponse(subjects,safe=False)

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
    if request.session.get('userid'):
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
    else:
        data = {'code':20001,'mesg':'please login first'}
    return JsonResponse(data)

def login(request: HttpRequest) -> HttpResponse:
    hint = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            password = gen_md5_digest(password)
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['userid'] = user.no
                request.session['username'] = user.username
                return redirect('/')
            else:
                hint = '用户名或密码错误'
        else:
            hint = '请输入有效的用户名和密码'
    return render(request, 'login.html', {'hint': hint})

def logout(request):
    """注销"""
    request.session.flush()
    return redirect('/')
        
def get_captcha(request: HttpRequest) -> HttpResponse:
    """验证码"""
    captcha_text = gen_random_code()
    request.session['captcha'] = captcha_text
    image_data = Captcha.instance().generate(captcha_text)
    return HttpResponse(image_data, content_type='image/png')           
    
