/**
 * Created by brayan on 09/10/15.
 */
/* Para manipular los eventos de la tabla*/

function eventos_tabla(tabla, boton){
    tabla.on('click', 'tr', function(){
         //Para obtener el id de la evaluacion de riesgo
        var $td = $(this).closest('tr').children('td');
        var id = $td.eq(0).text();

        //Para resaltar fila seleccionada
        $(this).addClass('highlight').siblings().removeClass('highlight');

        //Para agregar link a button detalles
        boton.prop("href","edit/"+id+ "/");
    });
}

