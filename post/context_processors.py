def is_author(request):
    if request.user.is_authenticated:
        return {
            'is_author': request.user.groups.filter(name='author').exists()
        }
    return {'is_author': False}



def notificationsView(request):


    if request.user.is_superuser  or request.user.is_staff:

        has_read_notifications= request.user.notifications.filter(is_read=False).exists

        return {
            'notifications':  request.user.notifications.order_by('-created_at')[:20],
             'has_read_notifications': has_read_notifications
        }
    return {'notifications': []}



from django.utils import timezone
from zoneinfo import ZoneInfo

utc_time = timezone.now()

kathmandu_time = utc_time.astimezone(ZoneInfo("Asia/Kathmandu"))  

def time(request):
    current_time = kathmandu_time.now()
    return {
        'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S')  # Format as needed
    }



def getcategories(request):
    from post.models import Category
    categories = Category.objects.all()
    return {
        'categorie': categories
    }



def popular_posts(request):
    from post.models import Post
    from django.db.models import Count

    posts = Post.objects.filter(is_draft=False)\
                        .annotate(num_postlikes=Count('postlike')) \
                        .order_by('-num_postlikes')[:4]

    return {
        'popular_posts': posts
    }

from .models import Post 

def getFooterpost(request):
    post=Post.objects.filter(is_draft=False)[:12]

    return {
        'footer_posts': post
    }



    



