from django.http import HttpResponseForbidden

def solo_padres_y_admins(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.tipo in ['padre', 'admin']:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view
