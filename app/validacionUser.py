from app.models import Empleado

def validacionUsuario(usuario):
    empleado = Empleado.objects.get(usuario=usuario)
    print('perfil empleado: %s' % empleado.perfil)
    return empleado.perfil