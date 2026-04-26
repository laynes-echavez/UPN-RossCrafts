"""
Formularios para el sistema de clientes
"""
from django import forms
from django.core.validators import RegexValidator
from apps.customers.models import Customer
import re


class CustomerRegisterForm(forms.Form):
    """Formulario de registro de clientes"""
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
        label='Nombre'
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
        label='Apellido'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        label='Email'
    )
    
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '987654321'}),
        label='Teléfono (opcional)'
    )
    
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        label='Contraseña'
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar Contraseña'
    )
    
    def clean_email(self):
        """Validar que el email sea único"""
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email
    
    def clean_password(self):
        """Validar que la contraseña tenga al menos un número"""
        password = self.cleaned_data.get('password')
        if not re.search(r'\d', password):
            raise forms.ValidationError('La contraseña debe contener al menos un número.')
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data


class CustomerLoginForm(forms.Form):
    """Formulario de inicio de sesión"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        label='Email'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Recordarme'
    )


_TW_INPUT = 'w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition'

class CustomerProfileForm(forms.ModelForm):
    """Formulario de edición de perfil"""

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': _TW_INPUT}),
            'last_name':  forms.TextInput(attrs={'class': _TW_INPUT}),
            'phone':      forms.TextInput(attrs={'class': _TW_INPUT}),
            'address':    forms.Textarea(attrs={'class': _TW_INPUT, 'rows': 3}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name':  'Apellido',
            'phone':      'Teléfono',
            'address':    'Dirección',
        }


class CustomerChangePasswordForm(forms.Form):
    """Formulario de cambio de contraseña"""
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña Actual'
    )
    
    new_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Nueva Contraseña'
    )
    
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar Nueva Contraseña'
    )
    
    def __init__(self, customer, *args, **kwargs):
        self.customer = customer
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        """Validar contraseña actual"""
        current_password = self.cleaned_data.get('current_password')
        if not self.customer.check_password(current_password):
            raise forms.ValidationError('La contraseña actual es incorrecta.')
        return current_password
    
    def clean_new_password(self):
        """Validar nueva contraseña"""
        password = self.cleaned_data.get('new_password')
        if not re.search(r'\d', password):
            raise forms.ValidationError('La contraseña debe contener al menos un número.')
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')
        
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data


class CustomerPasswordResetForm(forms.Form):
    """Formulario de solicitud de reset de contraseña"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        label='Email'
    )
