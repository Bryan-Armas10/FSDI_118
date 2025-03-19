from django import forms
from .models import Post, Message

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'body', 'status', 'image']

###### Message ######
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

####################################