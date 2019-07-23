from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from home.models import CPerson,student
from django.contrib.auth.models import User
from .models import Tutorial
# Create your views here
#tut_list=['Program structure','Basic Syntax','Datatypes','variables','Storage classes','Operators','Decision making','Loops','Functions','Scope rules','Arrays','Pointers','String','Structures','Unions','Bit Fields','Typedef','Input/Output','File I/O','Preprocessors','Header Files','Type casting','Error Handling','Recurssion','Variable Arguments','Memory management','Command Line Argument']
#@login_required(redirect_field_name='login')
@never_cache
def stu_home(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            stu=True
            tut_list=Tutorial.objects.all()
            context={
                'stu_first_name': request.user.first_name,
                'stu_last_name': request.user.last_name,
                'stu_email': request.user.email,
                'stu_collagename': activeuser.collage_name,
                'stu_progress': activeuser.progress,
                'tut_list':tut_list,
                'stu':stu,
            }
            return render(request,'tutorials/stu_home.html',context)
    else:
        return redirect('accounts:login')
    
def show_tutorial(request,tutorial_id):
    tut=True
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            tutorial=Tutorial.objects.get(pk=tutorial_id)
            tut_name=tutorial.name
            temp_name=tutorial.html_name
            pre_tut=get_pretut(tut_id=tutorial_id)
            next_tut=get_nexttut(tut_id=tutorial_id)
            preid=pre_tut.id
            nextid=next_tut.id
            pre_link = str(preid)
            next_link = str(nextid)
            stu_progress=activeuser.progress
            enable=True
            if is_progresstemplate(tutorial_id,stu_progress):
                enable=False
            context={
                'tut_id':tutorial_id,
                'tut_name':tut_name,
                'pre_link':pre_link,
                'next_link':next_link,
                'tut_list':tut_list,
                'stu_progress': stu_progress,
                'enable':enable,
                'tut':tut,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
    
def get_pretut(tut_id):
    if tut_id==1:
        return Tutorial.objects.get(pk=1)
    while True:
        tut_id=tut_id-1
        pre_tut=Tutorial.objects.filter(pk=tut_id).first()
        if pre_tut:
            return pre_tut
        
def get_nexttut(tut_id):
    while True:
        tut_id=tut_id+1
        next_tut=Tutorial.objects.filter(pk=tut_id).first()
        if next_tut:
            return next_tut
        

def is_progresstemplate(tut_id,progress):
    c=0
    temp_id=1
    while temp_id<=tut_id:
        if Tutorial.objects.filter(pk=temp_id).first():
            c=c+1
        temp_id=temp_id+1
    if c==progress:
        return True
    else:
        return False
        
def arithmetic_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/arithmetic_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def relational_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/relational_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def logical_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/logical_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def bitwise_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/bitwise_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
    
def assignment_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/assignment_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def misc_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/misc_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def precedence_example(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/precedence_example.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def if_statement(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/if_statement.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def ifelse_statement(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/ifelse_statement.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def nestedif_statement(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/nestedif_statement.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def switch_statement(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/switch_statement.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')
    
def nestedswitch_statement(request):
    if request.user.is_authenticated:
        try:
            cperson=CPerson.objects.get(user=request.user)
        except:
            return HttpResponse("You're not allowed to view this page.........")
        if cperson.type=='student':
            activeuser=student.objects.get(cperson=cperson)
            s="stu"
        if request.user.is_active and s=="stu":
            tut_list=Tutorial.objects.all()
            temp_name="tutorials/nestedswitch_statement.html"
            context={
                'tut_list':tut_list,
                'stu_progress': activeuser.progress,
            }
            return render(request,temp_name,context)
    else:
        return redirect('accounts:login')