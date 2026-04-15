from django.shortcuts import redirect
from django.http import HttpResponse

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        if(not request.user.is_staff):
            return HttpResponse("you are not authorized to access this page")
        return  view_func(request,*args,**kwargs)
    return wrapper_func