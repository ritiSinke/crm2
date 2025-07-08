def is_author(request):
    if request.user.is_authenticated:
        return {
            'is_author': request.user.groups.filter(name='author').exists()
        }
    return {'is_author': False}
