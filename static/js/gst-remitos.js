$(function () { 
    $(document).ready(function(){

        function cambiarTipoDetalle(selector){
            var tipoDetalle = document.getElementById($(selector).children().first().attr('id'));   
            var index = tipoDetalle.id.substring(0,10);
            if (tipoDetalle.options[tipoDetalle.selectedIndex].text === "Fraccionamiento"){
                $(selector).next().find('div.tambor').first().hide();
                $(selector).next().find('div.tambor').first().children()[0].selectedIndex = 0;
                $(selector).next().find('div.fraccionamiento').first().show();
            };
            if (tipoDetalle.options[tipoDetalle.selectedIndex].text === "Tambor"){
                $(selector).next().find('div.tambor').first().show();
                $(selector).next().find('div.fraccionamiento').first().children()[0].selectedIndex = 0;
                $(selector).next().find('div.fraccionamiento').first().hide();
            };       
        }; 

        function esValido(formulario){
            var errores = 0;
            $(formulario).find('.objetoDetalle').each(function(){                
                if (($(this).find('.tambor').children().first()[0].selectedIndex == '0') && ($(this).find('.fraccionamiento').children().first()[0].selectedIndex == '0')){                    
                    $(this).children().find('span').show();
                    $(this).children().filter('.tambor').first().addClass("alert alert-danger");
                    $(this).children().filter('.fraccionamiento').first().addClass("alert alert-danger");
                    errores += 1;
                } else {
                    $(this).children().find('span').hide()
                    $(this).children().filter('.tambor').first().removeClass("alert alert-danger");
                    $(this).children().filter('.fraccionamiento').first().removeClass("alert alert-danger");
                };
            });
            if (errores == 0){
                return true;
            } else {
                return false;
            };
        };


        function updateElementIndex(el, prefix, ndx) {
                var id_regex = new RegExp('(' + prefix + '-\\d+-)');
                var replacement = prefix + '-' + ndx + '-';
                if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
                if (el.id){
                     el.id = el.id.replace(id_regex, replacement);
                }
                if (el.name) el.name = el.name.replace(id_regex, replacement);
        };

        function deleteForm(btn, prefix) {
            var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
            if (formCount > 1) {
                // Delete the item/form
                $(btn).parents('.item').remove();
                var forms = $('.item'); // Get all the forms  
                // Update the total number of forms (1 less than before)
                $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
                var i = 0;
                // Go through the forms and set their indices, names and IDs
                for (formCount = forms.length; i < formCount; i++) {
                    $(forms.get(i)).children().children().each(function () {
                        if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
                    });
                }
            } // End if
            else {
                alert("Se debe ingresar como mínimo un detalle al Remito");
            }
            return false;
        };



        function addForm(btn, prefix) {
            //console.error(prefix);
            var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
            // You can only submit a maximum of 10 todo items 
            //console.error(formCount);
            // Clone a form (without event handlers) from the first form
            var row = $(".item:first").clone(false).get(0);
            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");

            // Relabel or rename all the relevant bits
            $(row).children().children().each(function (){
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
            });

            // Add an event handler for the tipo detalle selector
            $(row).find('.tipoDetalle').change(function(){
                return cambiarTipoDetalle($(this));
            });
            // Escondo el combo de fraccionamiento por defecto viene con tambor
            //$(row).find('.fraccionamiento').hide();
            //$(row).find('.tambor').show();

            $(row).find('.tipoDetalle').children().find("option:contains('Tambor')").attr('selected','selected');
            

            // Add an event handler for the delete item/form link 
            $(row).find("#delete").click(function () {
                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);

            // Fijo por defecto el tipo de detalle en tambor, selecciona el combobox de tambor            
            cambiarTipoDetalle($(row).find('.tipoDetalle'));
            
            // Seteo alert an row nuevos si exisen alertas            
            alertas = $('.objetoDetalle').find('.alert-danger');
            if (alertas.length > 0){                
                $(row).find('span').show();
                $(row).find('.tambor').addClass("alert alert-danger");
                $(row).find('.fraccionamiento').addClass("alert alert-danger");
            };
            
            //return false;
        };

        $('#guardar').on('click', function(){
            formulario = $('#formRemito').first();
            valido = esValido(formulario);
            if (valido){
                formulario.submit();
            };
        });
        
        //$('.help-inline').hide();
        //console.log($('.help-inline'));

        $('.fraccionamiento').hide();

        $('.tipoDetalle').change(function(){
            return cambiarTipoDetalle($(this));
        });

        // Register the click event handlers
        $("#add").click(function () {
            return addForm(this, "form");
        });

        $("#delete").click(function () {
            return deleteForm(this, "form");
        });    

                
    }); 
});