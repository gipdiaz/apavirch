function ingresarLote () {
    open("/lotes/ingresar-lote/","_self");
}
function editarLote (id) {
    open("/lotes/editar-lote/" + id,"_self");
}
function eliminarLote (id) {
    open("/lotes/eliminar-lote/" + id,"_self");
}
$(function () {
    
    function extraer (lote) {
        alert (lote.id);
        $.ajax({
            url: '/lotes/extraer-lote/',
            type: 'GET',
            data: {id: lote.id},
            context : lote,
        })
        .done(function(msj) {
            $(lote).removeClass('btn btn-warning btn-xs').addClass('btn btn-primary btn-xs');
            $(lote).text("Devolver");
            
            label = "#lb-estado-"+this.id;
            $(label).removeClass('label label-success').addClass('label label-warning');
            $(label).text("Extraido");
        })
        .fail(function(msj) {
            alert(msj);
        })
    }

    var divformpeso =   '<div class="center">'
                            +'<form id="formpeso" action="">'
                                +'<h4>Ingrese el peso extraido del lote</h4>'
                                +'<input type="text" name="peso"></input><br/>'
                            +'</form>';
                        +'</div>';

    $(document).ready(function(){

        $('.btn-accion').tooltip();
        
        $('#tabla-lotes').dataTable({
            "oLanguage": {
                "sUrl": "/static/js/libs/datatables/language.es.json",
            },
            "oSearch": {"sSearch": "Initial search"},
            
        });
        
        //-- Manejador de los botones de estado --//
        $(".btn-estado").click( function() {
            if ($(this).text() == "Extraer") {
                var btn = this;
                bootbox.confirm(divformpeso, function(result) {
                    if (result) {
                        var peso = parseInt($('#formpeso').find("input[name=peso]").val(), 10);
                        var pesolote = parseInt($(btn).closest('tr').find('td:eq(3)').text(), 10);
                        if ((peso > 0) && (peso < pesolote)) {
                            $.ajax({
                                url: '/lotes/extraer-lote/',
                                type: 'GET',
                                data: {id: btn.id,peso: peso},
                                context : btn,
                            })
                            .done(function(msj) {
                                $(btn).removeClass('btn btn-warning btn-xs').addClass('btn btn-primary btn-xs');
                                $(btn).text("Devolver");
                                
                                label = "#lb-estado-"+this.id;
                                $(label).removeClass('label label-success').addClass('label label-warning');
                                $(label).text("Extraido");
                            })
                            .fail(function(msj) {
                                alert(msj);
                            })  
                        }
                        else{
                            alert("El peso extraido debe ser mayor que cero y menor que el peso del lote");
                        };
                    }
                });
            };
            if ($(this).text() == "Devolver") {
                $.ajax({
                    url: '/lotes/devolver-lote/',
                    type: 'GET',
                    data: {id: this.id},
                    context : this,
                })
                .done(function(msj) {
                    $(this).removeClass('btn btn-primary btn-xs').addClass('btn btn-danger btn-xs');
                    $(this).html('<span class="glyphicon glyphicon-ban-circle"></span>');
                    $(this).attr("disabled", "disabled");
                    
                    label = "#lb-estado-"+this.id
                    $(label).removeClass('label label-warning').addClass('label label-primary');
                    $(label).text("Devuelto");
                })
                .fail(function( msj ) {
                    alert(msj);
                })
            };
        });
        $(".btn-extraccion").click( function() {
            var idLote = $(this).closest('tr').find('td:eq(0)').text();
            $("#modal-extraer").load("/lotes/lote-extraido/"+idLote);
        }); 
    }); 
});