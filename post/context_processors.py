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
            'notifications':  request.user.notifications.order_by('-created_at')[:10],
             'has_read_notifications': has_read_notifications
        }
    return {'notifications': []}
    
