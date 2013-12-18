function ingresarRemito () {
    open("/remitos/ingresar-remito/","_self");
}
function editarRemito (id) {
    open("/remitos/editar-remito/" + id,"_self");
}
function eliminarRemito (id) {
    open("/remitos/eliminar-remito/" + id,"_self");
}
 

$(function () { 
    $(document).ready(function(){
        //----   seteo el contexto de la tabla que contiene remitos  -----
        $('#tabla-remitos').dataTable({
            "oLanguage": {
                "sUrl": "/static/js/libs/datatables/language.es.json"
            },
            "aaSorting": [[ 0, "desc" ]],
        });   

        $('.btn-accion').tooltip();

        $(".btn-accion").click( function() {
            var idRemito = $(this).closest('tr').find('td:eq(0)').text();
            $("#modal-remito").load("/remitos/ver-remito/"+idRemito);
        });
    });
});
