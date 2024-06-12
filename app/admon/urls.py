from django.urls import path
from .views import HomeAdmin,UserListView, UserCreateView, UserUpdateView, UserDeleteView, GroupListView, GroupCreateView, GroupUpdateView,GroupDeleteView, ContactView

app_name = 'admon'

urlpatterns = [
    path('custom-admin/contacto', ContactView.as_view(), name='contact_form'),
    path('custom-admin/', HomeAdmin.as_view(), name='admin_home'),
    path('custom-admin/users/', UserListView.as_view(), name='user_list'),
    path('custom-admin/users/add/', UserCreateView.as_view(), name='user_add'),
    path('custom-admin/users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('custom-admin/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('custom-admin/groups/', GroupListView.as_view(), name='group_list'),
    path('custom-admin/groups/add/', GroupCreateView.as_view(), name='group_add'),
    path('custom-admin/groups/<int:pk>/edit/', GroupUpdateView.as_view(), name='group_edit'),
    path('custom-admin/groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),
]
