function ComprobarCaja(){
    var fecha=$('#fechaApertura').val();
    if (fecha != ''){
       console.log('hola');
       $('#controlarCierre').prop('action', '/Caja/cerrar/');
       $('#cerrarCaja').prop('type', 'submit');
       document.getElementById("cerrarCaja").click();
    }else{
       alert('No se realizó la apertura de caja')
       document.location.href='/Caja/apertura/'
    }

}
