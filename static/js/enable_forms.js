    $(document).ready(function() {
        // Проверяем статус подтверждения email при загрузке страницы
        var emailConfirmed = {% if user.email_confirmed %} true {% else %} false {% endif %};

        // Если email подтвержден, разрешаем редактирование полей
        if (emailConfirmed) {
            // Разблокируем все поля формы
//            $('#postForm input').removeAttr('readonly');
            // Разблокируем кнопку отправки формы
            $('#postForm button[type="submit"]').removeAttr('disabled');
        } else {
            // Если email не подтвержден, блокируем все поля формы
//            $('#postForm input').attr('readonly', 'readonly');
            // Блокируем кнопку отправки формы
            $('#postForm button[type="submit"]').attr('disabled', 'disabled');
        }
