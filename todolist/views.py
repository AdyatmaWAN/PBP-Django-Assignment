from django.core import serializers
from django.shortcuts import render

from todolist.models import TodoListItems
from todolist.forms import CreateTaskForm

from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from django.urls import reverse

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("todolist:show_todolist"))  # membuat response
            #response.set_cookie('last_login',
            #                    str(datetime.now()))  # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    #response.delete_cookie('last_login')
    return response


@login_required(login_url='/todolist/login/')
def show_todolist(request):
    #data_todolist = TodoListItems.objects.filter(user_id = request.user.id)
    #context = {
    #'list_todolist': data_todolist,
    #'nama': request.user.username,
    #'last_login': request.COOKIES['last_login'],
   # }
    return render(request, 'alt-todolist.html')

@login_required(login_url='/todolist/login/')
def create_task(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            todolistitem = TodoListItems(
                user = request.user,
                date = datetime.now(),
                title = form.cleaned_data['tittle'],
                description = form.cleaned_data['description'],
                is_finished = False
            )
            todolistitem.save()
            return HttpResponseRedirect("/todolist")
    else:
        form = CreateTaskForm()
    return render(request, "create-task.html", { "form" : form })

@login_required(login_url='/todolist/login/')
def delete_task(request, id):
    todolistitem = TodoListItems.objects.get(id=id)
    todolistitem.delete()
    return HttpResponseRedirect("/todolist")

@login_required(login_url='/todolist/login/')
def change_status(request, id):
    todolistitem = TodoListItems.objects.get(id=id)
    if todolistitem.is_finished:
        todolistitem.is_finished = False
    else:
        todolistitem.is_finished = True
    todolistitem.save()
    return HttpResponseRedirect("/todolist")

@login_required(login_url="/todolist/login")
def show_todolist_json(request):
    tasks = TodoListItems.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', tasks), content_type='application/json')

def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        new_task = TodoListItems(user=request.user, title=title, description=description, date=datetime.now())
        new_task.save()
        return HttpResponse(b"CREATED", status=20)
    return HttpResponseNotFound()

def delete_task2(request, id):
    task = TodoListItems.objects.get(id=id)
    task.delete()
    return HttpResponse(b"DELETED", status=200)

def change_status(request, id):
    task = TodoListItems.objects.get(id=id)
    task.is_finished = not task.is_finished
    task.save()
    return HttpResponse(b"CHANGED", status=200)