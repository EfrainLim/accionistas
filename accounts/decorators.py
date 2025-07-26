from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def aprobado_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'estado') and request.user.estado != 'A':
            return redirect('logout')
        return view_func(request, *args, **kwargs)
    return _wrapped_view 