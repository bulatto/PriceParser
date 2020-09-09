$(function(){
    // Отправка формы при нажатии на кнопку "Ввести"
    $("#checkbox").change(function() {
        if (this.checked != true) {
            // TODO: переделать в AJAX запрос и сделать красивое уведомление
            document.querySelector("#product_adding_form").submit();
        }
    });
});