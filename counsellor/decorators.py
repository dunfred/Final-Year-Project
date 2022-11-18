import functools
from django.shortcuts import redirect
from django.contrib import messages

from counsellor.models import Consent


# def client_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user:login_client'):
    
#     print(redirect_field_name)
#     actual_decorator = user_passes_test(
#         lambda u: hasattr(u, 'user_type'),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


def client_required(view_func, redirect_url="counsellor:login_client"):
    '''
    Decorator for views that checks that the logged in user is a client,
    redirects to the log-in page if necessary.
    '''
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'user_type'):
                return view_func(request,*args, **kwargs)

        return redirect(redirect_url)
    return wrapper


def consent_approval_taken(view_func, redirect_url="counsellor:confidential"):
    '''
    Decorator for views that checks that the logged in user is a client,
    redirects to the consent form page if they haven't filled yet.
    '''
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # print(request.META.get('HTTP_REFERER'))
        if request.user.is_authenticated:
            if Consent.objects.filter(user=request.user).exists():
                return view_func(request,*args, **kwargs)
        return redirect(redirect_url)
    return wrapper