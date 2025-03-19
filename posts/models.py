from django.db import models
from django.contrib.auth import get_user_model

class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256)
    author = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        Status,
        null=True,
        default=None,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="media/posts/", blank=True, null=True)

    def __str__(self):
        return self.title

###### Message ######
# class Message(models.Model):
#     author = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
#     message = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.message 
    
###################################################################################

class Message(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

