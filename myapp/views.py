from django.shortcuts import render, redirect  # Added redirect to imports
from .models import Product, Category , Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , SetPasswordForm
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAdress
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm , UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart





def search(request):
    if request.method == "POST":
     searched = request.POST['searched'] 
     searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
     if not searched:
            messages.success(request, "That Product Do Not Exist...")
            return render(request, 'search.html', {})
     else:
         
          return render(request, 'search.html', {'searched':searched})

    else:
     return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        # Get or create Profile
        current_user, created = Profile.objects.get_or_create(user=request.user)
        
        # Get or create ShippingAdress - adjust this based on your model structure
        try:
            shipping_user = ShippingAdress.objects.get(id=request.user.id)
        except ShippingAdress.DoesNotExist:
            shipping_user = ShippingAdress.objects.create(id=request.user.id)
        
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            if form.is_valid() and shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "Your Info Has Been Updated successfully.")
                return redirect('home')
            else:
                messages.error(request, "Please correct the error(s) below.")
        
        # Make sure both forms are passed to the template
        return render(request, 'update_info.html', {
            'form': form,
            'shipping_form': shipping_form
        })
    else:
        messages.error(request, "You must be logged in to update your profile.")
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Did they fill out the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            # Is the form valid?
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated successfully.")
                return redirect('login')  # Redirect to login after password change
            else:
                # Handle form errors
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            # Initialize the form for GET request
            form = ChangePasswordForm(user=current_user)

        return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, "You must be logged in to update your password.")
        return redirect('home')



def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if request.method == 'POST':
            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, "User has been updated successfully.")
                return redirect('home')
            else:
                messages.error(request, "Please correct the error(s) below.")

        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, "You must be logged in to update your profile.")
        return redirect('login')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})




def category(request, foo):
    foo = foo.replace('-', '')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(Category=category)
        return render(request, 'category.html', {'products': products, 'category': category})

    except:
        messages.success(request, ("That category? Never heard of her 💅 Try picking one that hasn’t ghosted us!"))
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    product = Product.objects.all()
    return render(request, 'home.html', {'products': product})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Get or create the profile
            current_user, created = Profile.objects.get_or_create(user=user)
            saved_cart = current_user.old_cart

            # Fix indentation in this section
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You did it! You're in! 🎉 Welcome to the land of the logged-in!")
            return redirect('home')
        else:
            messages.success(request, "Oops! The password fairy didn't bless your login this time. Try again! 🧚‍♂️")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You’ve logged out. The internet is a little quieter now. See you soon! 👋")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You did it! The internet has officially accepted you. 🎉")
            return redirect('update_info')
        else:
            messages.success(request, "Welp... that didn’t work. Try again, brave warrior 🧙‍♂️")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
