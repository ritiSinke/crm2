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
    # is_published = models.BooleanField(default=False)   
    scheduled_date = models.DateTimeField(null=True, blank=True)


class PostLike(models.Model):
    reader= models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(null=True, editable=True, default=0)

