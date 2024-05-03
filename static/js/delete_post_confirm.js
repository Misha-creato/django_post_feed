$(document).ready(function() {

  $('#deleteBtn').click(function() {
    var postId = $(this).data('postId');
    $('#confirmDeleteBtn').data('postId', postId); // Устанавливаем postId в атрибуте data-confirm-post-id для кнопки подтверждения удаления
    $('#deleteModal').modal('show'); // Показываем модальное окно для подтверждения удаления
  });

  $('#confirmDeleteBtn').click(function() {
    var postId = $(this).data('postId');
    // Здесь можно добавить логику удаления поста
    $('#deleteModal').modal('hide'); // Скрываем модальное окно после удаления
  });
});
