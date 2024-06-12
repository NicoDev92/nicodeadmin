

function procesarCampo(input) {
    var value = input.value.trim();
    if (value !== '') {
        // Verificar si el valor contiene solo caracteres numéricos y un máximo de un punto decimal
        if (/^[\d.]+$/.test(value)) {
            // Reemplazar comas por puntos para asegurar un formato válido
            input.value = value.replace(/,/g, '.');
            return parseFloat(input.value);
        }
    }
}

function validarNumros(valor, msj, is_error) {
    if (isNaN(valor)) {
        mensaje(msj, is_error);
        return false;
    } else {
        return true;
    }
}

function valorSugerido() {
    var precio_costo = document.getElementById("id_precio_costo");
    var porcentaje_fijo = document.getElementById("id_porcentaje_fijo");
    var porcentaje_variable = document.getElementById("id_porcentaje_variable");
    var porcentaje_ganancia = document.getElementById("id_porcentaje_ganancia");

    var precio_costo_value = procesarCampo(precio_costo);
    var porcentaje_fijo_value = procesarCampo(porcentaje_fijo);
    var porcentaje_variable_value = procesarCampo(porcentaje_variable);
    var porcentaje_ganancia_value = procesarCampo(porcentaje_ganancia);

    if (validarNumros(porcentaje_fijo_value, "El porcentaje de costo fijo debe ser numérico. Sin símbolos", true)
        && validarNumros(porcentaje_variable_value, "El porcentaje de costo variable debe ser numérico. Sin símbolos", true)
        && validarNumros(porcentaje_ganancia_value, "El porcentaje de ganancia debe ser numérico. Sin símbolos", true)
        && validarNumros(precio_costo_value, "El valor del precio de costo debe ser numérico. Sin símbolos", true)) {

        var precio_con_costos = precio_costo_value + (precio_costo_value * (porcentaje_fijo_value / 100)) + (precio_costo_value * (porcentaje_variable_value / 100));
        var precio_con_ganancia = precio_con_costos + (precio_con_costos * (porcentaje_ganancia_value / 100));


        $("#precio_sugerido").text(precio_con_ganancia.toFixed(2));
    }
}
