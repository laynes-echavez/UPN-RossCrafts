from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from apps.audit.models import AuditLog
from .models import User
from .decorators import role_required
from .mixins import RoleRequiredMixin
from .forms import UserCreateForm, UserUpdateForm, UserPasswordResetForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@ratelimit(key='ip', rate='5/15m', method='POST', block=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('authentication:dashboard_redirect')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            AuditLog.objects.create(
                user=user, action='LOGIN', url=request.path,
                ip_address=get_client_ip(request), status_code=200
            )
            messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}')
            return redirect('authentication:dashboard_redirect')
        else:
            AuditLog.objects.create(
                user=None, action='LOGIN_FAIL', url=request.path,
                ip_address=get_client_ip(request), status_code=401
            )
            messages.error(request, 'Credenciales inválidas. Por favor, intenta nuevamente.')

    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    is_employee = hasattr(request.user, 'role')
    if is_employee:
        AuditLog.objects.create(
            user=request.user, action='LOGOUT', url=request.path,
            ip_address=get_client_ip(request), status_code=200
        )
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    # Solo empleados usan este logout, siempre redirigir al login de empleados
    return redirect('authentication:login')


@login_required
def dashboard_redirect(request):
    user = request.user
    if not hasattr(user, 'role'):
        return redirect('ecommerce:catalog')
    if user.role == 'gerente':
        return redirect('reports:dashboard')
    elif user.role == 'administrador':
        return redirect('reports:dashboard')  # Administradores también van al dashboard
    elif user.role == 'empleado':
        return redirect('sales:pos')  # Solo empleados van al POS
    return redirect('authentication:login')


def access_denied(request):
    return render(request, 'authentication/access_denied.html')


# ── Gestión de usuarios del sistema ──────────────────────────────────────────

class UserListView(RoleRequiredMixin, ListView):
    allowed_roles = ['gerente']
    model = User
    template_name = 'authentication/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        qs = User.objects.order_by('last_name', 'first_name')
        search = self.request.GET.get('search', '')
        role = self.request.GET.get('role', '')
        is_active = self.request.GET.get('is_active', '')

        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        if role:
            qs = qs.filter(role=role)
        if is_active == '1':
            qs = qs.filter(is_active=True)
        elif is_active == '0':
            qs = qs.filter(is_active=False)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_role'] = self.request.GET.get('role', '')
        ctx['selected_is_active'] = self.request.GET.get('is_active', '')
        ctx['role_choices'] = User.ROLE_CHOICES
        return ctx


class UserCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['gerente']
    model = User
    form_class = UserCreateForm
    template_name = 'authentication/user_form.html'
    success_url = reverse_lazy('authentication:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'Usuario "{form.instance.username}" creado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Crear'
        return ctx


class UserUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['gerente']
    model = User
    form_class = UserUpdateForm
    template_name = 'authentication/user_form.html'
    success_url = reverse_lazy('authentication:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'Usuario "{form.instance.username}" actualizado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Editar'
        return ctx


@login_required
@role_required(['gerente'])
def user_toggle_active(request, pk):
    """Activar / desactivar usuario"""
    user = get_object_or_404(User, pk=pk)

    # No permitir desactivarse a sí mismo
    if user == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('authentication:user_list')

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        estado = 'activado' if user.is_active else 'desactivado'
        messages.success(request, f'Usuario "{user.username}" {estado} exitosamente.')
        return redirect('authentication:user_list')

    return render(request, 'authentication/user_confirm_toggle.html', {'object': user})


@login_required
@role_required(['gerente'])
def user_reset_password(request, pk):
    """Cambiar contraseña de un usuario"""
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, f'Contraseña de "{user.username}" actualizada exitosamente.')
            return redirect('authentication:user_list')
    else:
        form = UserPasswordResetForm()

    return render(request, 'authentication/user_reset_password.html', {'form': form, 'object': user})
