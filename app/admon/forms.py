from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.db.models import Q

# Formulario de creación de usuarios
class UserCreateForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['groups'].widget.attrs.update({
            'class': 'form-check-input'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.save_m2m()
        return user

# Formulario de edición de usuarios
class UserEditForm(UserChangeForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff', 'is_superuser', 'groups', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control w-100'
            })
        self.fields['groups'].widget.attrs.update({
            'class': 'form-check-input'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.save_m2m()
        return user

class GroupForm(forms.ModelForm):
    # Filtrar permisos no deseados
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir permisos de Administración, Autenticación y Autorización, y los permisos 'Can delete'
        excluded_permissions = Permission.objects.filter(
            Q(content_type__app_label='admin') |
            Q(content_type__app_label='auth') |
            Q(name__icontains='Can delete')
        )
        self.fields['permissions'].queryset = Permission.objects.exclude(id__in=excluded_permissions)

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),  # Placeholder queryset, will be set in __init__
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
