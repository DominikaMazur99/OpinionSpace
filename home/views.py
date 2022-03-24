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
            form.save()
            return redirect('home:home')
    else:
        form = UserForm()

    return render(request, 'home/signup.html', {'form': form})

def item(request):
    AddItem = modelformset_factory(Item, fields=['name', 'description', 'authors', 'year', 'user'], max_num=1, extra=2)

    if request.method == 'POST':
        add_item = AddItem(request.POST)
        if add_item.is_valid():
            add_item.save()
            return redirect('home:home')
    else:
        add_item = AddItem(queryset=Item.objects.none())
    return render(request, 'home/add_item.html', {'add_item': add_item})

def item_view(request):
    if request.method == 'GET':
        items = Item.objects.all()
        ctx = {"items": items}
        return render(request, "home/item_view.html", ctx)