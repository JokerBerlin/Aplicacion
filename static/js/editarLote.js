$(document).ready(function() {
  //$('#id_Total').text("0.00");
  $("#generarAlmacen").click(function() {
    var num=1;
    productos = [];
    contador = 0;
    error = "";
    $('#tabla tbody tr').each(function (index) {
      // productosPedido = [];
      // var id = $(this).find("td").eq(0).html();
      // var cantidad = $(this).find("td").eq(1).html();
      // console.log(codigo);
      $(this).children("td").each(function (index2) {
          producto = [];
          //dato = index;
          console.log(index);
          switch (index2) {
              case 0:
                  id = $(this).text();
              case 3:
                  cantidad = $("#cantidad"+index ).val();

          }

      });
      contador = 1;
      productos.push([id,cantidad]);
      });
      console.log(productos);

      if (contador == 1) {
          var lote = $('#lote_id').val();
          var datos = {productos: productos};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/Lote/editar/"+lote+"/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,

              success: function (response) {
              //     var id_venta = result["id_venta"];
                  if(response['error']=='error'){
                      alert("El lote no se puede editar");
                      document.location.href='/Lote/listar/';
                  }else{
                      alert('Lote modificado');
                      //location.reload(true);
                      document.location.href='/Lote/listar/';
                  }


              }
          });
      }else{
          alert("No registró ningún producto");
      }


  });



});
