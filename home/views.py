from random import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from home.forms import UserForm, AddItemForm, AddCommentForm
from home.models import Item, Comment


class HomeView(View):
    def get(self, request):
        items = Item.objects.all().order_by('-likes')
        items_list = list(items)
        ctx = {'item1': items_list[0], 'item2': items_list[1], 'item3': items_list[2]}
        return render(request, "home/home.html", ctx)

    def post(self, request):
        return render(request, 'home/home.html')


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


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Item.objects.get(pk=pk)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Item.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)



class PostDisplay(DetailView):
    model = Item
    template_name = 'home/item_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        return context


class ItemEditView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'authors', 'year', 'user', 'category']
    template_name = 'home/edit_item.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been changed successfully.')
        return reverse_lazy('home:home')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class DeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    fields = ["name"]
    template_name = 'home/delete_item.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("home:home")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


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


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["content"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been updated successfully.')
        return reverse_lazy("home:item_details")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    fields = ["content"]
    template_name = 'home/delete_comment.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("home:home")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'home/edit_comment.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Your comment has been changed successfully.')
        return reverse_lazy('home:home')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
