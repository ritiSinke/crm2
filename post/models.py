from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    is_draft= models.CharField(
        max_length=15,
        choices=(
            ('True', 'True'),
            ('False', 'False')
        ),
        default ='True',
    )
   
    image= models.ImageField( upload_to='images', null=True, blank=True)


class PostLike(models.Model):
    reader= models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(null=True, editable=True, default=0)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    is_delete=models.BooleanField(default=False)

    parents=models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies',blank=True, null=True)





class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)