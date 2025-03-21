from django.shortcuts import render, redirect
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Status
from .forms import MessageForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_posts = Post.objects.all()
        context["post_list"] = all_posts.order_by("created_on").reverse()
        return context
    
class PostDetailView(DetailView):
    template_name= "posts/detail.html"
    model = Post

    #### Message ####

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all()
        form = MessageForm()
        context['comments'] = comments
        context['form'] = form
        return context
        
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=post.id)  
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['form_errors'] = form.errors
            return self.render_to_response(context)
            # context['form'] = form
            # context['form_errors'] = form.errors 

    #############################


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
