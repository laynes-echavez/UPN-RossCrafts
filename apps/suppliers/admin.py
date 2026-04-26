from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_name', 'email', 'phone', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['company_name', 'contact_name', 'email', 'ruc']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['supplier__company_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_cost', 'subtotal']
    search_fields = ['product__name', 'order__id']
