from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from home.models import *
from django.shortcuts import get_object_or_404
from django.http import Http404
from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN , endpoint='https://test.instamojo.com/api/1.1/')

def home(request):
    pizzas = Pizza.objects.all()  # Fetch all pizzas
    return render(request, 'home.html', {'pizzas': pizzas})
def base(request):
    return render(request , 'base.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')  # Use the URL name here
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')  # Use the URL name here
    
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')  # Use the URL name here
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')  # Use the URL name here
        
        try:
            user = User.objects.create(username=username)
            user.set_password(password1)
            user.save()
            messages.success(request, "Account has been created successfully")
            return redirect('login')  # Use the URL name here
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')  # Use the URL name here
    
    return render(request, 'register.html')



def add_cart(request, pizza_id):
    user = request.user
    pizza_obj = get_object_or_404(Pizza, uuid=pizza_id)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    
    if not CartItems.objects.filter(cart=cart, pizza=pizza_obj).exists():
        CartItems.objects.create(
            cart=cart,
            pizza=pizza_obj
        )
    
    return redirect('home')



def order(request):
    try:
        # Fetch the user's cart
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist for this user.")
    
    # Make a payment request
    response = api.payment_request_create(
        amount=cart.total(),
        purpose="Order",
        buyer_name=request.user.username,
        email=request.user.email,
        redirect_url="http://127.0.0.1:8000/confirmorder"
    )
    
    cart_items = CartItems.objects.filter(cart=cart)
    total_cost = sum(item.pizza.price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    
    
    return render(request, 'confirm_order.html', context)

def delete_cart_item(request, cart_item_uid):
    try:
        CartItems.objects.get(pk=cart_item_uid).delete()
        return redirect('cartorder')
    except Exception as e:
        print(e)
        return redirect('cartorder')



def confrim_order(request):
    return render(request , 'confrim_order.html')