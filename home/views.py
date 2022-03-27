from random import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from home.forms import UserForm, AddItemForm
from home.models import Item, Comment


def home(request):
    if request.method == 'GET':
        return render(request, "home/home.html")



def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration succesful.')
            return redirect('home:home')
        messages.error(request, 'Unsuccessful registration. Invalid information')
    else:
        form = UserForm()

    return render(request, 'home/signup.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="home/login.html", context={"login_form": form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home:home')

def item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        # breakpoint()
        if form.is_valid():
            form.save()
            return redirect('home:home')
    else:
        form = AddItemForm()
    return render(request, 'home/add_item.html', {'add_item': form})

def item_view(request):
    items_list = Item.objects.all()
    paginator = Paginator(items_list, 2)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    ctx = {"items": items}
    return render(request, "home/item_view.html", ctx)


def item_details(request,id):
    item_details = Item.objects.get(id=id)
    try:
        item_comments = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        item_comments = None

    ctx = {'itemId': item_details, 'comments': item_comments}
    return render(request, 'home/item_details.html', ctx)

def comment(request):
    AddComment = modelformset_factory(Comment, fields=['name', 'content'], max_num=1, extra=2)
    if request.method == 'POST':
        add_comment = AddComment(request.POST)
        if add_comment.is_valid():
            add_comment.save()
            return redirect('home:home')
    else:
        add_comment = AddComment(
            queryset=Item.objects.none(),
        )
    return render(request, 'home/add_comment.html', {'add_comment': add_comment})

