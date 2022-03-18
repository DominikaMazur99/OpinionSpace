from django.shortcuts import render, redirect
from home.forms import UserForm


def home(request):
    return render(request, "home/home.html")


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home:home')
    else:
        form = UserForm()

    return render(request, 'home/signup.html', {'form': form})
