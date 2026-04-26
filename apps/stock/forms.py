"""
Formularios para la gestión de productos y stock
"""
from django import forms
from .models import Product, Category, StockMovement


class ProductForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'category', 'description',
            'price', 'cost_price', 'stock_quantity',
            'min_stock_quantity', 'image', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU único'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del producto'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Precio de venta'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Precio de costo'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en stock'}),
            'min_stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock mínimo'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nombre',
            'sku': 'SKU',
            'category': 'Categoría',
            'description': 'Descripción',
            'price': 'Precio de Venta',
            'cost_price': 'Precio de Costo',
            'stock_quantity': 'Cantidad en Stock',
            'min_stock_quantity': 'Stock Mínimo',
            'image': 'Imagen',
            'is_active': 'Activo',
        }


class CategoryForm(forms.ModelForm):
    """Formulario para crear/editar categorías"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StockMovementForm(forms.ModelForm):
    """Formulario para registrar movimientos de stock"""
    
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reason']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ImportExcelForm(forms.Form):
    """Formulario para importar productos desde Excel"""
    file = forms.FileField(
        label='Archivo Excel',
        help_text='Formato: .xlsx o .xls',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        })
    )
