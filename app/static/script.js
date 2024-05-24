$(document).ready(function() {
    $('#recommendationForm').on('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        var formData = $(this).serialize(); // Coleta os dados do formulário

        $('#loading-overlay').fadeIn(); // Mostra o overlay de carregamento após o envio do formulário

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            success: function(response) {
                $('#loading-overlay').fadeOut(); // Esconde o overlay de carregamento
                $('body').html(response); // Substitui o conteúdo do corpo pela resposta do servidor
            },
            error: function() {
                $('#loading-overlay').fadeOut(); // Esconde o overlay de carregamento
                $('#alert').removeClass('d-none').text('Ocorreu um erro ao obter as recomendações. Tente novamente.');
            }
        });
    });
});
