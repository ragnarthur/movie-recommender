$(document).ready(function() {
    $('#recommendationForm').on('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        var formData = $(this).serialize(); // Coleta os dados do formulário

        // Mostra o overlay de carregamento após o envio do formulário
        $('#loading-overlay').fadeIn('fast');

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            success: function(response) {
                // Esconde o overlay de carregamento
                $('#loading-overlay').fadeOut('fast');
                // Substitui o conteúdo do corpo pela resposta do servidor
                $('body').html(response);
            },
            error: function() {
                // Esconde o overlay de carregamento
                $('#loading-overlay').fadeOut('fast');
                // Exibe mensagem de erro
                $('#alert').removeClass('d-none').text('Ocorreu um erro ao obter as recomendações. Tente novamente.');
            }
        });
    });
});
