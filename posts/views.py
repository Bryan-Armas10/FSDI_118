from django.shortcuts import render, redirect
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Status, Comment
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.decorators import login_required # function view
from django.contrib.auth.mixins import LoginRequiredMixin # class view
from django.core.exceptions import PermissionDenied

"""
Class-based views:

View        = generic view
ListView    = get a list of records
DetailView  = get a single(detail) record
CreateView  = create a new record
DeleteView  = remove a record
UpdateView  = modify an existing record
LoginView   = login
"""


# Create your views here.
class PostListView(ListView):
    template_name = "posts/list.html"
    model =Post

    def get_filtered_data(self, search):
        if search:
            print("Applying filter")
            results = Post.objects.filter(title__contains=search).order_by("created_on").reverse()
            return results
        else:
            return Post.objects.all().order_by("created_on").reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        all_posts = self.get_filtered_data(search_text)
        context["post_list"] = all_posts
        return context

    
class PostDetailView(DetailView):
    template_name= "posts/detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Read all the comments for the post
        post = self.object
        comments = Comment.objects.filter(post=post)
        context["comments"] = comments

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/create.html"
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "posts/update.html"
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post_list")

    def get_object(self, queryset = None):
        post = super().get_object(queryset)

        if post.author != self.request.user:
            raise PermissionDenied("You don't have permission to modify this rercord!")
        else:
            return post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/delete.html"
    success_url = reverse_lazy("post_list")

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        if post.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post!")
        else:
            return post


# Funtion based views

def create_comment(request):
    # get data
    post_id = request.POST.get("post_id")
    comment_text = request.POST.get("comment")
    user = request.user
    post = Post.objects.get(id=post_id)

    # Create the comment record
    comment = Comment.objects.create(
        author = user,
        content = comment_text,
        post=post
    )
    comment.save()

    return redirect("post_detail", pk=post_id)
