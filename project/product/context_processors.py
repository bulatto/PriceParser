from django.urls import reverse


def add_navigation_links(request):
    """Контекстный процессор для передачи название элементов навигации и ссылок
    на них в шаблон
    """
    return {
        'navigation_links': [
            ('Просмотр товаров', reverse('product:show_goods')),
            ('Контакты', ''),
            ('О сайте', '')
        ]
    }
