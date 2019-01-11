"""ferreteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from app.Views.productoView import *
from app.Views.precioView import *
from app.Views.presentacionView import *
from app.Views.aperturacajaView import *
from app.Views.cierrecajaView import *
from app.Views.operacionView import *
from app.Views.pedidoView import *
from app.Views.usuarioView import *
from app.Views.clienteView import *
from app.Views.rutaView import *
from app.Views.visitaView import *
from app.Views.errorView import *
from app.Views.proveedorView import *
from app.Views.ventaView import *
from app.Views.reciboView import *
from app.Views.loteView import *
from app.Views.almacenView import *
from app.Views.cajaView import *

###########################################################
#   Usuario: Erick Sulca, Ulises Bejar
#   Fecha: 05/06/18
#   Última modificación:
#   Descripción: url registrarError
###########################################################

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^home/$', Home),
    url(r'^Home/$', Home),
    url(r'^prueba/$', Prueba),

    ################## Caja #######################
    url(r'^Caja/apertura/$', registrarAperturacaja),
    url(r'^Caja/cierre/$', cierreCaja),
    url(r'^Caja/movimiento/$', registrarOperacion),

    ################## Venta #######################
    #vista nueva venta
    url(r'^Venta/nuevo/$', ventaNuevo),
    url(r'^Venta/registrar/$', insertarVenta),
    url(r'^Pedido/nuevo/$', registrarPedido),
    #url(r'^venta/insertar/$', registrarPedido),
    url(r'^Pedido/registrar/$', insertarPedido),

    ################## Producto #######################
    url(r'^Producto/listar/$', ListarProductos, name='listar_producto'),
    url(r'^Producto/nuevo/$', registrarProducto),
    url(r'^Presentacion/nuevo/$', registrarPresentacion),
    url(r'^Presentacion/editar/$', editarPresentacion),
    url(r'^Producto/detalle/(?P<producto_id>\d+)/$', detalleProducto),
    url(r'^Producto/editar/(?P<producto_id>\d+)/$', editarProducto),
    url(r'^Producto/eliminar/$', eliminar_identificador_producto,name='eliminar_producto'),
    url(r'^Lote/nuevo/$', registrarLote),
    url(r'^Lote/listar/$', listarLote),
    url(r'^Lote/detalle/(?P<lote_id>\d+)/$', detalleLote),


    ################## Catalogo #######################
    url(r'^Presentacion/Listar/(?P<producto_id>\d+)/$', presentacion_detalle),
    url(r'^Presentacion/registrar/$', registrarPresentacionProducto),
    url(r'^Presentacion/eliminar/(?P<presentacion_id>\d+)/(?P<producto_id>\d+)/$', eliminarPresentacionProducto),
    url(r'^Presentacion/getPresentaciones/$', getPresentaciones),

    url(r'^Precios/getPrecios/$', getPrecios),
    #url(r'^pruebaExcel/$', IngresarPrecios),

    ################## Cliente #######################
    url(r'^Cliente/nuevo/$', nuevoCliente),
    url(r'^Cliente/Registrar/$', registrarCliente),

    url(r'^Cliente/detalle/(?P<cliente_id>\d+)/$', detalleCliente),
    url(r'^Cliente/editar/(?P<cliente_id>\d+)/$', editarCliente),
    url(r'^Cliente/listar/$', listarCliente, name="listar_cliente"),
    url(r'^Cliente/eliminar/$', eliminar_identificador_cliente, name="eliminar_cliente"),
    #url(r'^Cliente/buscar/$', IngresarPrecios),
    url(r'^Cliente/actualizar/$', IngresarPrecios),
    #url(r'eliminar_identificador/$', eliminar_identificador_cliente, name='eliminar_identificador'),

    ################## Pedidos #######################

    url(r'^Pedido/nuevo/$', registrarPedido),
    url(r'^Pedido/listar/$', ListarPedidos),
    url(r'^Pedido/listar/(?P<estado_id>\d+)/$', ListarEstadoPedidos),
    url(r'^Pedido/modificar/$', modificarPedido),

    url(r'^Pedido/resumen/$', ResumenPedidos),
    url(r'^Pedido/detalle/(?P<pedido_id>\d+)/$', DetallePedido),
    url(r'^Pedido/editar/(?P<pedido_id>\d+)/$', editarPedido),
    url(r'^Pedido/venta/(?P<pedido_id>\d+)/$', pedidoVenta),
    url(r'^Pedido/venta/', pedidoVenta),

    url(r'^Pedido/eliminar/$', eliminar_identificador_pedido,name="eliminar_pedido"),
    url(r'^Pedido/actualizar/$', IngresarPrecios),
    url(r'^Pedido/reporte/$', IngresarPrecios),
    url(r'^Pedido/buscar/$', IngresarPrecios),
    url(r'^Pedido/imprimir/$', IngresarPrecios),
    url(r'^imprimir/(?P<venta_id>\d+)/$', imprimir),
    ################## RUTA #######################
    url(r'^Ruta/nuevo/$', registrarRuta),
    url(r'^Ruta/listar/$',listarRutas),
    url(r'^Ruta/detalle/(?P<ruta_id>\d+)/$', detalleRuta),

    ################## APP Movil #######################
    url(r'^usuario/validar/$', validarUsuario),
    url(r'^usuario/ruta/$', rutaUsuario),

    url(r'^usuario/visita/cancelar/$', cancelarVisita),
    url(r'^usuario/visita/reiniciar/$', reiniciarVisita),

    url(r'^cliente/buscar/$', buscarCliente),
    url(r'^cliente/detalle/$', detalleClienteWS),

    url(r'^pedido/insertar/$', InstarPedido),
    url(r'^pedido/listar/$', ListarPedido),
    url(r'^pedido/detalle/$', DetallePedidoMovil),
    url(r'^pedido/editar/$', DetallePedidoMovil),
    url(r'^pago/nuevo/$', IngresarPrecios),
    url(r'^pedido/venta/$', pedidoVenta),


    url(r'^producto/buscar/$', BuscarProducto),
    url(r'^productopre/buscar/$', BuscarProductoPresentacion),
    url(r'^producto-pre-venta/buscar/$', BuscarProductoPresentacionVenta),
    url(r'^producto/presentacion/listar/$', ListarPresentacionesProducto),
    url(r'^producto/presentacion/cantidad/$', CantidadPresentacionesProducto),

    url(r'^error/registrar/$', registrarError),
    url(r'^ruta/insertar/$', registrarRuta),

    url(r'^lote/insertar/$', registrarLote),

    url(r'^proveedor/buscar/$', BuscarProveedor),
    url(r'^Proveedor/Registrar/$', registrarProveedor),

    url(r'^almacen/buscar/$', BuscarAlmacen),

    url(r'^recibo/buscar/$', BuscarRecibo),
#######################Ventas##############################

    #url(r'^venta/nuevo/$', registrarPedido),
    url(r'^Venta/listar/$', ListarVentas, name="venta_listar"),
    url(r'^Venta/anular/(?P<venta_id>\d+)/$', anularVenta),
    url(r'^Venta/detalle/(?P<venta_id>\d+)/$', DetalleVenta),


    #filtros de Ventas
    #url(r'^venta/filtrar/', filtrarVentas, name="filtrar_ventas"),
    url(r'^venta/filtras/', FiltrarVenta),
    url(r'^venta/filtrase/', guardar_cookies),
    url(r'^venta/filtrar/eliminar/', eliminar_cookies),
    url(r'^Pedido/filtrar/', FiltrarPedido),
    url(r'^Pedido/estado/(?P<estado_id>\d+)/$', EstadoPedido),
    url(r'^venta/eliminar/', eliminar_identificador_venta,name="eliminar_venta"),
    url(r'^venta/anular/', anularVenta),
    url(r'^error/', visualizarError),
    url(r'^error/cierreCaja-efectuado/', cierreCajaEfectuado),

    #url(r'^venta/filtrase/', leer),
    #
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/cliente/(?P<cliente>\w+)/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/cliente/(?P<cliente>\w+)/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/cliente/(?P<cliente>\w+)/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/cliente/(?P<cliente>\w+)/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/cliente/(?P<cliente>\w+)/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/cliente/(?P<cliente>\w+)/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/cliente/(?P<cliente>\w+)/$', Fentas),
    # url(r'^venta/filtrar/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/producto/(?P<producto_buscado>\w+)/$', Fentas),
    # url(r'^venta/filtrar/cliente/(?P<cliente>\w+)/$', Fentas),
    # url(r'^venta/filtrar/desde/(?P<inicio>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),
    # url(r'^venta/filtrar/hasta/(?P<fin>[0-9]{2}-?[0-9]{2}-?[0-9]{4})/', Fentas),


    #####################################################

#######################Rutas##############################

    #url(r'^Ruta/nuevo/$', nuevoVenta),
    #url(r'^Ruta/listar/$', ListarVenta),

#######################Información y Reportes##############################

    url(r'^Reporte/almacen/$', reporteAlmacen),
    url(r'^Reporte/almacen/salida-producto/$', salidaProductoAlmacen),
    url(r'^Reporte/almacen/cantidad-producto/$', cantidadProductoAlmacen),
    url(r'^Reporte/almacen/tiempo-pedido/$', tiempoPedidoAlmacen),

    url(r'^Reporte/caja/$', reporteCaja),
    url(r'^Reporte/caja/(?P<añoActual>\d+)/(?P<mesActual>\d+)/$', montoCajaActual),
    url(r'^Reporte/caja/(?P<cajaId>\d+)/(?P<añoActual>\d+)/(?P<mesActual>\d+)/$', movimientosCaja),

    url(r'^Reporte/ventas/$', reporteVentas),
    url(r'^Reporte/venta/empleado/(?P<añoActual>\d+)/(?P<mesActual>\d+)/$', todosEmpleadosVentas),
    url(r'^Reporte/venta/empleado/(?P<empleado_id>\d+)/(?P<añoActual>\d+)/(?P<mesActual>\d+)/$', empleadoVentas),
    url(r'^Reporte/ventas-anuladas/$', reporteVentasAnuladas),
    url(r'^Reporte/venta-anulada/empleado/(?P<añoActual>\d+)/(?P<mesActual>\d+)/$', todoMontoVentasAnuladas),
    url(r'^Reporte/venta-anulada/empleado/(?P<empleado_id>\d+)/(?P<añoActual>\d+)/(?P<mesActual>\d+)/$', ventasAnuladasReporte),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     # debug solo para desarrollo
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns