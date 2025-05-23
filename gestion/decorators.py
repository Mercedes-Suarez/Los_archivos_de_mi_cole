from django.shortcuts import redirect
from django.contrib import messages
from gestion.models import Padre
#from django.http import HttpResponseForbidden

def solo_admins(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acceso restringido solo a administradores.")
        return redirect('inicio')
    return _wrapped_view

def solo_admins_padres(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            try:
                if hasattr(request.user, 'padre'):
                    return view_func(request, *args, **kwargs)
            except Padre.DoesNotExist:
                pass
        messages.error(request, "Acceso restringido solo a administradores o padres.")
        return redirect('inicio')
    return _wrapped_view
