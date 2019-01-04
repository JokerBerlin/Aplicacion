from app.models import Empleado

def validacionUsuario(usuario):
    empleado = Empleado.objects.get(usuario=usuario)
    return empleado.perfil