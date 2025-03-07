from django.shortcuts import render
from django.views.generic import(
    ListView,
    DetailView
)
from .models import Post, Status

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
    template_name= "posts/list.html"
    model = Post