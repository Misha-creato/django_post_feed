$(document).ready(function() {

  $('.deleteBtn').click(function() {
    var postId = $(this).attr('id');
    $('#deleteModal'+postId).modal('show'); // Показываем модальное окно для подтверждения удаления
  });

});
