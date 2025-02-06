from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .middlewares import auth, guest
from .forms import ProductForm, UserRegistrationForm, AdminRegistrationForm
from .models import Product, CustomUser, ROLE_CHOICES, Admin, User, Role, ROLE_CHOICESS, Cart
# from .forms import AddressForm

@guest




def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if request.user.role in ['admin', 'superadmin']:
                user.created_by = request.user
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

def superadmin_dashboard(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.created_by = request.user
            user.role = 'admin'  # Set the role to admin by default
            user.save()
            # Create a corresponding entry in the Admin table
            role_instance = Role.objects.get(name='admin')
            Admin.objects.get_or_create(
                username=user.username,
                defaults={
                    'email': user.email,
                    'password': user.password,
                    'role': role_instance  # Assign the Role instance
                }
            )
            return redirect('superadmin_dashboard')
    else:
        form = AdminRegistrationForm()
    admins = Admin.objects.all()
    return render(request, 'dashboard/superadmin_dashboard.html', {'form': form, 'admins': admins})
# def superadmin_dashboard(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.created_by = request.user
#             user.save()
#             return redirect('superadmin_dashboard')
#     else:
#         form = UserRegistrationForm()
#     admins = Admin.objects.all()
#     return render(request, 'dashboard/superadmin_dashboard.html', {'form': form, 'admins': admins})




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
# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if request.user.role in ['admin', 'superadmin']:
#                 user.created_by = request.user
#             user.save()
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'auth/register.html', {'form': form})


# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'user'  # Set the role to user by default
#             if request.user.role in ['admin', 'superadmin']:
#                 user.created_by = request.user
#             user.save()
#             # Create a corresponding entry in the User table
#             if request.user.role in ['admin', 'superadmin']:
#                 try:
#                     admin = Admin.objects.get(username=request.user.username)
#                     User.objects.create(
#                         admin_id=admin.id,
#                         username=user.username,
#                         email=user.email,
#                         password=user.password
#                     )
#                 except Admin.DoesNotExist:
#                     # Handle the case where the Admin object does not exist
#                     pass
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'auth/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                if request.user.role in ['admin', 'superadmin']:
                    user.created_by = request.user
                    user.save()
                    # Create a corresponding entry in the User table
                    User.objects.create(
                        admin_id=request.user.id,
                        username=user.username,
                        email=user.email,
                        password=user.password
                    )
                    # If the user is a superadmin, create an entry in the Admin table
                    if request.user.role == 'superadmin':
                        role_instance = Role.objects.get(name='admin')
                        Admin.objects.get_or_create(
                            username=user.username,
                            defaults={
                                'email': user.email,
                                'password': user.password,
                                'role': role_instance  # Assign the Role instance
                            }
                        )
            except Admin.DoesNotExist:
                # Handle the case where the Admin object does not exist
                pass
            return redirect('login')
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

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_product')
    else:
        form = ProductForm()
    products = Product.objects.all()
    return render(request, 'create_product.html', {'form': form, 'products': products})

@login_required
def create_user_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'  # Set the role to user by default
            user.created_by = request.user
            user.save()
            return redirect('create_user')
    else:
        form = UserRegistrationForm()
    users = CustomUser.objects.filter(role='user')
    return render(request, 'auth/create_user.html', {'form': form, 'users': users})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={'price': product.price})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})