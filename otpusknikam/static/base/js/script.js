$(function() {

    $('.hover').hover(
      function() {
        $(this).find('.menu').show();
      }, function() {
        $(this).find('.menu').hide();
      }
    );

    $('.filter-form select').change(function() {
        $(this.form).submit();
    });

});
