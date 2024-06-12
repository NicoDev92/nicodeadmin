from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.

class SinAutorizacion(PermissionRequiredMixin):
    raise_exception=False
    redirect_field_name="redirect_to"
    def handle_no_permission(self):
        self.login_url="bases:forbidden"
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class Home(LoginRequiredMixin, generic.TemplateView):
    
    template_name = "bases/home.html"
    login_url = 'bases:login'

class HomeSinAutorizacion(generic.TemplateView):
    template_name = "bases/forbidden.html"


