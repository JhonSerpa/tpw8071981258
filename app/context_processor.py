from app.models import User


def add_var_to_context(request):

    try:
        User.objects.get(authentication_id=request.user.id) if request.user else None
        return {
            'app_user': User.objects.get(authentication_id=request.user.id) if request.user else None,
            'isadmin': request.user.is_superuser
        }
    except User.DoesNotExist:
        return {
            'isadmin': request.user.is_superuser
        }
