#  authenticated
from django.shortcuts import  redirect
def auth(view_function):
    def wrapped_view(request,*args,**kwargs):
        if request.user.is_authenticated == False:
            return redirect('login')
        return view_function(request, *args, **kwargs)
    return wrapped_view

# def guest(view_function):
#     def wrapped_view(request,*args,**kwargs):
#         if request.user.is_authenticated :
#             return redirect('dashboard')
#         return view_function(request, *args, **kwargs)
#     return wrapped_view 



def guest(view_function):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif request.user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        return view_function(request, *args, **kwargs)
    return wrapped_view