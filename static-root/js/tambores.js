$(function () {
    $(document).ready(function(){
        $('.btn-accion').tooltip();
        $(".btn-fraccionamiento").click( function() {
            var idTambor = $(this).closest('tr').find('td:eq(0)').text();
            $("#modal-fraccionamiento").load("/tambores/tambor-fraccionado/"+idTambor);
        }); 
    }); 
});