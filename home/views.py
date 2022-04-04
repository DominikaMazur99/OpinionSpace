from random import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from home.forms import UserForm, AddItemForm, AddCommentForm
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




class PostDisplay(DetailView):
    model = Item
    template_name = 'home/item_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        return context


class PostComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Item
    form_class = AddCommentForm
    template_name = 'home/item_details.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.item = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('home:item_details', kwargs={'pk': post.pk}) + '#comments'




