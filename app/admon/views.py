from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import GroupForm, UserCreateForm, UserEditForm
from django.http import JsonResponse
from django.db import IntegrityError

from django.views import generic


from django.contrib.auth.mixins import LoginRequiredMixin
from bases.views import SinAutorizacion


class HomeAdmin(LoginRequiredMixin, SinAutorizacion, generic.TemplateView):
    template_name = "custom_admin/admin_home.html"
    login_url = 'bases:login'
    permission_required = "auth.change_user" 

    def handle_no_permission(self):
        self.login_url = "bases:forbidden"
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class ContactView(LoginRequiredMixin, SinAutorizacion, generic.TemplateView):
    template_name = "custom_admin/contact_form.html"
    login_url = 'bases:login'
    permission_required = "auth.change_user"
    
    
class UserCreateView(LoginRequiredMixin, SinAutorizacion, generic.CreateView):
    model = User
    context_object_name = 'obj'
    form_class = UserCreateForm
    template_name = 'custom_admin/user_form.html'
    permission_required = "auth.change_user"
    success_url = reverse_lazy('admon:user_list')

    def form_valid(self, form):
        redirect_url = reverse_lazy("admon:user_list")
        try:
            return super().form_valid(form)
        except IntegrityError:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

class UserUpdateView(LoginRequiredMixin, SinAutorizacion, generic.UpdateView):
    model = User
    context_object_name = 'obj'
    form_class = UserEditForm
    template_name = 'custom_admin/user_form.html'
    permission_required = "auth.change_user"
    success_url = reverse_lazy('admon:user_list')

    def form_valid(self, form):
        redirect_url = reverse_lazy("admon:user_list")
        try:
            return super().form_valid(form)
        except IntegrityError:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)

class UserListView(LoginRequiredMixin, SinAutorizacion, generic.ListView):
    model = User
    permission_required = "auth.change_user"
    template_name = 'custom_admin/user_list.html'

class UserDeleteView(LoginRequiredMixin, SinAutorizacion, generic.DeleteView):
    model = User
    permission_required = "auth.change_user"
    success_url = reverse_lazy('admon:user_list')

class GroupListView(LoginRequiredMixin, SinAutorizacion, generic.ListView):
    model = Group
    context_object_name = "obj"
    permission_required = "auth.change_user"
    template_name = 'custom_admin/group_list.html'

class GroupCreateView(LoginRequiredMixin, SinAutorizacion, generic.CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'custom_admin/group_form.html'
    permission_required = "auth.change_user"
    success_url = reverse_lazy('admon:group_list')
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object

        # Permissions grouped by category
        context['proveedor_perms'] = Permission.objects.filter(id__in=[45, 46, 48])
        context['facturas_perms'] = Permission.objects.filter(id__in=[49, 50, 52])
        context['pagos_perms'] = Permission.objects.filter(id__in=[53, 54, 56])
        context['caja_perms'] = Permission.objects.filter(id__in=[57])
        context['inventario_perms'] = Permission.objects.filter(id__in=[25, 26, 28, 33, 34, 36, 69, 70, 72, 41, 42, 44, 29, 30, 32, 37, 38, 40])

        return context

class GroupUpdateView(LoginRequiredMixin, SinAutorizacion, generic.UpdateView):
    model = Group
    form_class = GroupForm
    context_object_name = 'obj'
    template_name = 'custom_admin/group_form.html'
    permission_required = "auth.change_user"
    success_url = reverse_lazy('admon:group_list')
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print(form.errors)
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return super().form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)
        else:
            return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object
        group_permissions = group.permissions.values_list('id', flat=True)

        # Permissions grouped by category
        context['proveedor_perms'] = Permission.objects.filter(id__in=[45, 46, 48])
        context['facturas_perms'] = Permission.objects.filter(id__in=[49, 50, 52])
        context['pagos_perms'] = Permission.objects.filter(id__in=[53, 54, 56])
        context['caja_perms'] = Permission.objects.filter(id__in=[57])
        context['inventario_perms'] = Permission.objects.filter(id__in=[25, 26, 28, 33, 34, 36, 69, 70, 72, 41, 42, 44, 29, 30, 32, 37, 38, 40])

        context['group_permissions'] = group_permissions
        return context

class GroupDeleteView(LoginRequiredMixin, SinAutorizacion, generic.DeleteView):
    model = Group
    permission_required = "auth.change_user"
    success_url = reverse_lazy('admon:group_list')  
