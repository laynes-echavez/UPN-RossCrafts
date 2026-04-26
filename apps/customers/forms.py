"""
Formularios para la gestión de clientes
"""
from django import forms
from django.core.validators import RegexValidator
from .models import Customer

_TW = 'w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition'


class CustomerForm(forms.ModelForm):
    dni = forms.CharField(
        max_length=8,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='El DNI debe tener exactamente 8 dígitos numéricos'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': _TW + ' font-mono',
            'placeholder': '12345678',
            'maxlength': '8',
        }),
        label='DNI'
    )

    phone = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{9,15}$',
                message='El teléfono debe tener entre 9 y 15 dígitos'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': _TW,
            'placeholder': '987654321',
        }),
        label='Teléfono'
    )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'dni', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': _TW, 'placeholder': 'Nombre'}),
            'last_name':  forms.TextInput(attrs={'class': _TW, 'placeholder': 'Apellido'}),
            'email':      forms.EmailInput(attrs={'class': _TW, 'placeholder': 'correo@ejemplo.com'}),
            'address':    forms.Textarea(attrs={'class': _TW, 'rows': 3, 'placeholder': 'Dirección completa'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name':  'Apellido',
            'email':      'Email',
            'phone':      'Teléfono',
            'dni':        'DNI',
            'address':    'Dirección',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Customer.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email
