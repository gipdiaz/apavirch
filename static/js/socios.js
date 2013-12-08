function ingresarSocio () {
    open("/socios/ingresar-socio/","_self");
}
function editarSocio (id) {
    open("/socios/editar-socio/" + id,"_self");
}
function eliminarSocio (id) {
    open("/socios/eliminar-socio/" + id,"_self");
}
 

$(function () { 
    $(document).ready(function(){
        $('#tabla-socios').dataTable({
            "oLanguage": {
                "sUrl": "/static/js/libs/datatables/language.es.json"
            },
        }); 

        //-- Manejador de los botones de estado --//
        $(".btn-estado").click( function() {
            if ($(this).text() == "Activar") {
                $.ajax({
                    url: '/socios/activar-socio/',
                    type: 'GET',
                    data: {id: this.id},
                    context : this,
                })
                .done(function(msj) {
                    $(this).removeClass('btn btn-warning btn-xs').addClass('btn btn-primary btn-xs');
                    $(this).text("Desactivar");
                    
                    label = "#lb-estado-"+this.id;
                    $(label).removeClass('label label-success').addClass('label label-warning');
                    $(label).text("Activo");
                })
                .fail(function(msj) {
                    alert('hubo un error');
                    alert(msj);
                })
            };
            if ($(this).text() == "Desactivar") {
                $.ajax({
                    url: '/socios/desactivar-socio/',
                    type: 'GET',
                    data: {id: this.id},
                    context : this,
                })
                .done(function(msj) {                    
                    label = "#lb-estado-"+this.id
                    $(label).removeClass('label label-warning').addClass('label label-primary');
                    $(label).text("Inactivo");
                    $(this).remove();

                    boton = "#btn_editar_"+this.id
                    $(boton).attr("disabled", "disabled");

                })
                .fail(function( msj ) {
                    alert(msj);
                })
            };

            if ($(this).text() == "Probar") {
                $.ajax({
                    url: '/socios/probar-socio/',
                    type: 'GET',
                    data: {codigoUnicoIdentif: this.codigoUnicoIdentif},
                    context : this,
                })
                .done(function(msj) {
                    $(this).removeClass('btn btn-warning btn-xs').addClass('btn btn-primary btn-xs');
                    $(this).text("Activar");   
                    
                    label = "#lb-estado-"+this.id
                    $(label).removeClass('label label-warning').addClass('label label-primary');
                    $(label).text("A Prueba");
                })
                .fail(function( msj ) {
                    alert(msj);
                })
            };
        }); 
    }); 
});
