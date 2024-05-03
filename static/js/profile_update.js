// Добавляем обработчики событий для кликов на иконки
$('#avatarEdit').click(function() {
    // Показываем модальное окно для редактирования аватара
    $('#avatarUpdateModal').modal('show');
});

$('#textEdit').click(function() {
    // Показываем модальное окно для редактирования текста
    $('#textModal').modal('show');
});

// Закрываем модальные окна при клике на крестик или вне модального окна
$(document).click(function(event) {
    if ($(event.target).is('#avatarUpdateModal') || $(event.target).is('#textModal')) {
        $('#avatarUpdateModal').modal('hide');
        $('#textModal').modal('hide');
    }
});
