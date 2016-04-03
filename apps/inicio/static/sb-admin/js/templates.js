/**
 * Created by brayan on 09/10/15.
 */
/* Para manipular los eventos de la tabla*/
var id;
var fila_selec;
function resalta_fila(fila_selec){
    //Para resaltar fila seleccionada
    fila_selec.addClass('highlight').siblings().removeClass('highlight');
}

function eventos_tabla(tabla){
    tabla.on('click', 'tr', function(){
         //Para obtener el id de la evaluacion de riesgo
        var $td = $(this).closest('tr').children('td');
        id = $td.eq(0).text();

        fila_selec = $(this);
        resalta_fila(fila_selec);
    });
}

function edicion_fila(boton){
    //Para agregar link a button detalles
    boton.prop("href","edit/"+id+ "/");
}

