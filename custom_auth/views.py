from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .middlewares import auth, guest
from .forms import ProductForm   #newww
from .models import Product   #neww

@guest
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username' :'','password1':'','password2':''}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html',{"form":form})

    

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username' :'','password1':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html',{"form":form})

@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')
def logout_view(request):
    logout(request)
    return redirect('login')

# Create your views here.


# def dashboard_view(request):   #newwww
#     products = Product.objects.all()  # Fetch all products
#     return render(request, 'dashboard.html', {'products': products})


def create_product(request):   #newww
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after creating the product
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


def dashboard_view(request):    #neww
    products = Product.objects.all()  # Fetch all products
    return render(request, 'dashboard.html', {'products': products})