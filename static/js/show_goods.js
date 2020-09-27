$(function(){
    var current_url = new URL(window.location.href),
        only_with_photo_param = 'only_with_photo',
        only_with_photo_checkbox = document.querySelector('#only_with_photo');

    // Отправка формы при нажатии на кнопку "Ввести"
    $("#checkbox").change(function() {
        if (this.checked != true) {
            // TODO: переделать в AJAX запрос и сделать красивое уведомление
            document.querySelector("#product_adding_form").submit();
        }
    });

    // Проставление чекбокса "Только с фото", если параметр задан в запросе
    if (current_url.searchParams.has(only_with_photo_param)) {
        only_with_photo_checkbox.checked = current_url.searchParams.get(
            only_with_photo_param) == 'true';
    }

    // Перенаправление на новый url при смене статуса чекбоскса "Только с фото"
    $("#only_with_photo").change(function() {
        var new_url = new URL(window.location.href);
        is_checked = only_with_photo_checkbox.checked;
        new_url.searchParams.set(only_with_photo_param, is_checked);
        window.location.href = new_url;
    });

});