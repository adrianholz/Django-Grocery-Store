from django.urls import path
from . import views
from .views import add_to_basket, view_basket, product_detail, product_list, customer_account, CustomLoginView, buy_basket

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('products/', product_list, name='product_list'),
    path('product/<str:product_id>/', product_detail, name='product_detail'),
    path('product/<str:product_id>/add/', add_to_basket, name='add_to_basket'),
    path('basket/', view_basket, name='view_basket'),
    path('account/', customer_account, name='customer_account'),
    path('buy-basket/<int:basket_id>/', buy_basket, name='buy_basket'),
]
