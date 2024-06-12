

function mensaje(message, isError) {
    $('#message_content').text(message);
    if (isError) {
        $('#btn-modal').removeAttr("href");
    } else {
        $('#btn-modal').attr("href", "{% url 'inv:categoria_list' %}");
    }
    $('#popup').modal('show');
}