from django.shortcuts import redirect
from django.contrib import messages
#from django.http import HttpResponseForbidden

def solo_admins(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.usuario.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acceso restringido solo a administradores.")
        return redirect('inicio')
    return _wrapped_view

def solo_padres_y_admins(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo in ['padre', 'admin']:
            return view_func(request, *args, **kwargs)
        return redirect("No tienes permiso para acceder a esta vista.")
    return _wrapped_view