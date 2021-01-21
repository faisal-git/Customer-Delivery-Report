from django.http import HttpResponse
from django.shortcuts import redirect

def checkIfAuthenticated(view_fun):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fun(request,*args,**kwargs)
    return wrapper


def adminOnly(allowed_groups=set()):
    def userIsAdminOrCustomer(view_fun):
        def wrapper(request,*args,**kwargs):
            
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_groups:
                        return view_fun(request,*args,**kwargs)
                
            
            return redirect('userProfile')
        return wrapper
    return userIsAdminOrCustomer


def checkPermission(allowed_groups=set()):
    def userIsAdminOrCustomer(view_fun):
        def wrapper(request,*args,**kwargs):
            
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_groups:
                        return view_fun(request,*args,**kwargs)
                
            
            return HttpResponse('You are not authorized to view user')
        return wrapper
    return userIsAdminOrCustomer