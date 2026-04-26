from django import forms
from django.core.validators import RegexValidator
from .models import Supplier, PurchaseOrder, PurchaseOrderItem

_TW = 'w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition'
_TW_SELECT = _TW + ' bg-white'


class SupplierForm(forms.ModelForm):
    ruc = forms.CharField(
        max_length=11,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='El RUC debe tener exactamente 11 dígitos numéricos'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': _TW,
            'placeholder': 'RUC de 11 dígitos',
            'maxlength': '11',
        })
    )

    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_name', 'email', 'phone', 'address', 'ruc', 'is_active']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': _TW, 'placeholder': 'Nombre de la empresa'}),
            'contact_name': forms.TextInput(attrs={'class': _TW, 'placeholder': 'Nombre del contacto'}),
            'email':        forms.EmailInput(attrs={'class': _TW, 'placeholder': 'email@ejemplo.com'}),
            'phone':        forms.TextInput(attrs={'class': _TW, 'placeholder': 'Teléfono'}),
            'address':      forms.Textarea(attrs={'class': _TW, 'rows': 3, 'placeholder': 'Dirección completa'}),
            'is_active':    forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary/30'}),
        }
        labels = {
            'company_name': 'Nombre de la Empresa',
            'contact_name': 'Nombre del Contacto',
            'email':        'Email',
            'phone':        'Teléfono',
            'address':      'Dirección',
            'ruc':          'RUC',
            'is_active':    'Proveedor activo',
        }


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': _TW_SELECT}),
            'notes':    forms.Textarea(attrs={'class': _TW, 'rows': 3, 'placeholder': 'Notas adicionales (opcional)'}),
        }
        labels = {
            'supplier': 'Proveedor',
            'notes':    'Notas',
        }


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'unit_cost']
        widgets = {
            'product':   forms.Select(attrs={'class': _TW_SELECT + ' product-select'}),
            'quantity':  forms.NumberInput(attrs={'class': _TW + ' quantity-input', 'min': '1', 'value': '1'}),
            'unit_cost': forms.NumberInput(attrs={'class': _TW + ' cost-input', 'step': '0.01', 'min': '0.01'}),
        }
