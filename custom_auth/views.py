from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .middlewares import auth, guest
from .forms import ProductForm, UserRegistrationForm
from .models import Product, CustomUser, ROLE_CHOICES, Admin, User

@guest



# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if request.user.role == 'admin':
#                 user.created_by = request.user
#             user.save()
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'auth/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if request.user.role == 'admin':
                user.admin = Admin.objects.get(username=request.user.username)
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        selected_role = request.POST.get('role')
        if form.is_valid():
            user = form.get_user()
            if user.role == selected_role:
                login(request, user)
                if user.role == 'superadmin':
                    return redirect('superadmin_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                form.add_error(None, 'Role does not match.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form, 'roles': ROLE_CHOICES})
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             if user.role == 'superadmin':
#                 return redirect('superadmin_dashboard')
#             elif user.role == 'admin':
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('user_dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'auth/login.html', {'form': form})

@auth
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
# def superadmin_dashboard_view(request):
#     products = Product.objects.all()
#     return render(request, 'dashboard/superadmin_dashboard.html', {'products': products})

# def superadmin_dashboard_view(request):
#     if request.user.role != 'superadmin':
#         return redirect('login')  # Redirect to login or an appropriate page
#     products = Product.objects.all()
#     return render(request, 'dashboard/superadmin_dashboard.html', {'products': products})
# def superadmin_dashboard_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     if request.user.role != 'superadmin':
#         return redirect('login')  
#     products = Product.objects.all()
#     return render(request, 'dashboard/superadmin_dashboard.html', {'products': products})
# from .decorators import role_required

# @role_required('superadmin')
def superadmin_dashboard_view(request):
    if request.user.role != 'superadmin':
        return redirect('login')  # Redirect to login or an appropriate page
    products = Product.objects.all()
    return render(request, 'dashboard/superadmin_dashboard.html', {'products': products})

@login_required
def admin_dashboard_view(request):
    if request.user.role != 'admin':
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'products': products})
# def admin_dashboard_view(request):
#     if request.user.role not in ['admin', 'superadmin']:
#         return redirect('login')  # Redirect to login or an appropriate page
#     products = Product.objects.all()
#     return render(request, 'dashboard/admin_dashboard.html', {'products': products})

@login_required
# def user_dashboard_view(request):
#     products = Product.objects.all()
#     return render(request, 'dashboard/user_dashboard.html', {'products': products})
def user_dashboard_view(request):
    if request.user.role != 'user':
        return redirect('login')  # Redirect to login or an appropriate page
    products = Product.objects.all()
    return render(request, 'dashboard/user_dashboard.html', {'products': products})

@login_required
# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = ProductForm()
#     return render(request, 'create_product.html', {'form': form})

def create_product(request):
    if request.user.role not in ['admin', 'superadmin', 'user']:
        return redirect('login')  # Redirect to login or an appropriate page
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif request.user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

@login_required
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('superadmin_dashboard')  # Redirect to the appropriate dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})



@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    if request.user.role == 'superadmin':
        return redirect('superadmin_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            if request.user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif request.user.role == 'admin':
                return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form, 'product': product})



@login_required
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'view_product.html', {'product': product})











# def dashboard_view(request):
#     products = Product.objects.all()
#     return render(request, 'dashboard.html', {'products': products})





# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import login_required
# from .middlewares import auth, guest
# from .forms import UserRegistrationForm, ProductForm
# from .models import Product, CustomUser

# @guest
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             if user.role == 'superadmin':
#                 return redirect('superadmin_dashboard')
#             elif user.role == 'admin':
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('user_dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'auth/login.html', {'form': form})

# @auth
# def logout_view(request):
#     logout(request)
#     return redirect('login')

# @login_required
# def superadmin_dashboard_view(request):
#     if request.user.role != 'superadmin':
#         return redirect('login')  # Redirect to login or an appropriate page
#     products = Product.objects.all()
#     return render(request, 'dashboard/superadmin_dashboard.html', {'products': products})

# @login_required
# def admin_dashboard_view(request):
#     if request.user.role not in ['admin', 'superadmin']:
#         return redirect('login')  # Redirect to login or an appropriate page
#     products = Product.objects.all()
#     return render(request, 'dashboard/admin_dashboard.html', {'products': products})

# @login_required
# def user_dashboard_view(request):
#     if request.user.role != 'user':
#         return redirect('login')  # Redirect to login or an appropriate page
#     return render(request, 'dashboard/user_dashboard.html')

# @login_required
# def create_product(request):
#     if request.user.role not in ['admin', 'superadmin']:
#         return redirect('login')  # Redirect to login or an appropriate page
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')
#     else:
#         form = ProductForm()
#     return render(request, 'create_product.html', {'form': form})

# @guest
# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'auth/register.html', {'form': form})


