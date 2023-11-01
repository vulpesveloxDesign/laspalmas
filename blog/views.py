from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post
from .forms import PostCreateForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['category_wise_sorted_posts'] = Post.objects.custom_category_dict()  # you can pass filter logic as well, like Posts.objects.custom_category_dict(author_id=1)
        # context = super().get_context_data(**kwargs)
        return context


class PostDetailView(DetailView):
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    model = Post
    success_url = '/post/{slug}'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostCreateForm
    model = Post
    success_url = '/post/{slug}'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
