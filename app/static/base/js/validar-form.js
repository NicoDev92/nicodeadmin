
function submitForm() {
    $('form').submit(function (event) {
        event.preventDefault();

        var formSelector = $(this).data('form-selector');
        var formUrl = $(this).data('form-url');

        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (data) {
                mensaje("Guardado satisfactoriamente.", false);

                setTimeout(function () {
                    $('#popup').modal('hide');
                    window.location.replace(formUrl);
                }, 3000); // 3000 milisegundos (3 segundos)
            },
            error: function (xhr, status, error) {
                var errorMessage = '';
                if (xhr.responseJSON.errors && Object.keys(xhr.responseJSON.errors).length > 0) {
                    for (var field in xhr.responseJSON.errors) {
                        var errorList = xhr.responseJSON.errors[field];
                        for (var i = 0; i < errorList.length; i++) {
                            errorMessage += errorList[i] + '\n';
                        }
                    }
                } else {
                    errorMessage = 'Se produjo un error al procesar la solicitud.';
                }

                mensaje(errorMessage, true);
            }
        });
    });
}

// Llamamos a la función cuando el documento esté listo
$(document).ready(function () {
    submitForm();
});
