from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect ,get_object_or_404
from todo.models import  Task
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required 


@login_required(login_url ='login')
def task(request):
    all_task = Task.objects.filter(is_completed = False).order_by('-updated_at')
    completed_task = Task.objects.filter(is_completed = True).order_by('updated_at')
    
    context = {
        'all_task' : all_task,
        'completed_task':completed_task         
    }
    
    return render(request,'task_home.html',context)

    

def home(request):
    if request.method =="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = UserForm()
    context = {
        'form':form
    }
    return render(request,'home.html',context)



@login_required(login_url ='login')
def mark_as_done(request,id):
    mark_as_done = get_object_or_404(Task, id=id)
    mark_as_done.is_completed = True
    mark_as_done.save()
    return redirect('task')

@login_required(login_url ='login')
def mark_as_undone(request,id):
    mark_as_undone = get_object_or_404(Task,id=id)
    mark_as_undone.is_completed = False
    mark_as_undone.save()
    return redirect('task')


@login_required(login_url ='login')
def add_task(request):
    if request.method == 'POST':
        add_task = request.POST.get('add_task')
        if add_task and add_task.strip():  # Check if add_task is not None and not empty With White Space 
            Task.objects.create(task=add_task.strip())
            return redirect('task')
        else:
            return redirect('task')
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
    
@login_required(login_url ='login')
def edit_task(request,id):
    get_task = get_object_or_404(Task,id=id)
    if request.method == 'POST':
        update_task = request.POST['update_task']
        get_task.task = update_task
        get_task.save()
        return redirect('task')
    
    context = {
        'get_task':get_task,
    }
    return render(request,'edit_task.html',context)


@login_required(login_url ='login')
def delete_task(req,id):
    delete_task = get_object_or_404(Task,id=id)
    delete_task.delete()
    return redirect('task')


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('task')
                
    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request,'login.html',context)


def logout(request):
    auth.logout(request)
    return redirect('login')