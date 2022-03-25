from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from home.forms import UserForm
from home.models import Item



def home(request):
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
    AddItem = modelformset_factory(Item, fields=['name', 'description', 'authors', 'year', 'user', 'category'], max_num=1, extra=2)
    if request.method == 'POST':
        add_item = AddItem(request.POST)
        if add_item.is_valid():
            add_item.save()
            return redirect('home:home')
    else:
        add_item = AddItem(
            queryset=Item.objects.none(),
        )
    return render(request, 'home/add_item.html', {'add_item': add_item})

def item_view(request):
    if request.method == 'GET':
        items = Item.objects.all()
        ctx = {"items": items}
        return render(request, "home/item_view.html", ctx)