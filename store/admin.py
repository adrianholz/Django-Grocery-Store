from django.contrib import admin
from .models import Product, Basket, BasketItem, Purchase

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price')
    search_fields = ('name',)
    fields = ('product_id', 'name', 'price', 'image')  # Include the image field

class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0

class PurchaseInline(admin.TabularInline):  # Create an inline for Purchase
    model = Purchase
    extra = 0

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    inlines = [BasketItemInline, PurchaseInline]  # Include PurchaseInline here

    def approve_basket(self, request, queryset):
        queryset.update(approved=True)
        for basket in queryset:
            # Create a Purchase record when a basket is approved
            Purchase.objects.create(customer=basket.customer, basket=basket)

    def deny_basket(self, request, queryset):
        queryset.update(approved=False)

    actions = [approve_basket, deny_basket]

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'basket', 'purchased_at')  # Include purchased_at for display
    list_filter = ('purchased_at',)
