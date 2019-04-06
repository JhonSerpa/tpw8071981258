
def add_var_to_context(request):
    return {
        'isadmin': request.user.is_superuser
    }
