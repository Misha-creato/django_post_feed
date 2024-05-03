// Находим изображение профиля и модальное окно
var avatarImg = $('.avatar');
var modal = $('#avatarModal');

// Находим изображение внутри модального окна
var modalImg = $('#avatarModalImg');

// Функция открытия модального окна при клике на изображение профиля
avatarImg.click(function() {
    modal.modal('show');
    modalImg.attr('src', $(this).attr('src'));
});

// Функция закрытия модального окна при клике на крестик
var closeButton = $('.close');
closeButton.click(function() {
    modal.modal('hide');
});

// Закрытие модального окна при клике вне картинки
$(document).click(function(event) {
    if ($(event.target).is(modal)) {
        modal.modal('hide');
    }
});
