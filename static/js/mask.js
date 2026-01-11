
//Mascara para telefone fixo e celular
$(document).ready(function(){
  $('.mask_fone').mask('(00) 00000-0000'); // padrão celular
  // Ajuste dinâmico para fixo ou celular
  $('.mask_fone').on('blur', function() {
    var phone = $(this).val().replace(/\D/g, '');
    if(phone.length === 10) {
      $(this).mask('(00) 0000-0000');
    } else {
      $(this).mask('(00) 00000-0000');
    }
  });
});

//Mascara para CEP
$(document).ready(function(){
  // aplica máscara de CEP em todos os inputs com classe "cep"
  $('.mask_cep').mask('00000-000');
});

//mascara para valor monetário
$(document).ready(function(){
  $('.mask_number').mask('000.000.000.000.000,00', {reverse: true});
});
