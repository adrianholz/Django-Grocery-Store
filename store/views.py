from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import logout
from django.utils import timezone

# Import User model and Purchase model
from django.contrib.auth.models import User
from .models import Customer, Product, Basket, BasketItem, Purchase  # Ensure Purchase is imported

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

@staff_member_required
def staff_dashboard(request):
    return render(request, 'store/staff_dashboard.html')

def home(request):
    return render(request, 'store/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_basket(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    basket, created = Basket.objects.get_or_create(customer=request.user, approved=False)
    basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

    basket_item.quantity += quantity
    basket_item.save()

    return redirect('product_list')

def approve_basket(self, request, queryset):
    for basket in queryset:
        basket.approved = True
        basket.save()
        # Create a Purchase record
        Purchase.objects.create(customer=basket.customer, basket=basket)

@login_required
def view_basket(request):
    basket = Basket.objects.filter(customer=request.user, approved=False).first()
    return render(request, 'store/basket.html', {'basket': basket})

@login_required
def buy_basket(request, basket_id):
    basket = Basket.objects.filter(id=basket_id, customer=request.user, approved=True).first()
    
    if basket:
        # Create a Purchase record before deleting the basket
        Purchase.objects.create(customer=request.user, basket=basket)
        basket.delete()

    return redirect('customer_account')


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('customer_account')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def customer_account(request):
    basket = Basket.objects.filter(customer=request.user).order_by('-created_at').first()
    purchases = Purchase.objects.filter(customer=request.user).order_by('-purchased_at')

    return render(request, 'store/customer_account.html', {'basket': basket, 'purchases': purchases})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse('admin:index')
        else:
            return reverse('customer_account')

def custom_logout(request):
    logout(request)
    return redirect('/')
