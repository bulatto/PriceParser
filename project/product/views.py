from collections import namedtuple

from django.db.models import BooleanField
from django.db.models import Case
from django.db.models import Q
from django.db.models import When
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View

from common.helpers import add_get_param_to_url
from common.helpers import get_sort_dir
from common.helpers import pagination_page

from .forms import UrlForm
from .helpers import GOODS_ON_PAGE
from .helpers import add_url
from .helpers import delete_site
from .helpers import prepare_products
from .models import Product


class ShowGoodsView(View):

    # Исходный запрос
    queryset = Product.products_with_prices.annotate(has_photo=Case(
        When(Q(photo_path__isnull=False) | Q(photo_path=''), then=True),
        default=False, output_field=BooleanField()))

    # Словарь, описывающий доступные сортировки
    sorting_dict = {
        'created': {
            'verbose_name': 'Дата добавления',
            'order_list': {
                'asc': ['created', 'current_price', '-has_photo'],
                'desc': ['-created', 'current_price', '-has_photo'],
            }
        },
        'current_price': {
            'verbose_name': 'Цена',
            'order_list': {
                'asc': ['current_price', '-has_photo', '-created'],
                'desc': ['-current_price', '-has_photo', '-created'],
            }
        },
    }

    @classmethod
    def _apply_sorting(cls, products_query, sort_code, sort_dir=None):
        """Применение сортировки к запросу

        :param products_query: Запрос к модели
        :param sort_code: Значение переменной сортировки из запроса request
        :param sort_dir: Направление сортировки (asc или desc)

        :return: Изменённый запрос с сортировкой, текущий код сортировки
        """
        # Если указанной сортировки, то берётся по умолчанию created
        if not sort_code or sort_code not in cls.sorting_dict:
            sort_code = 'created'

        try:
            order_list = cls.sorting_dict[sort_code]['order_list'][sort_dir]
            products_query = products_query.order_by(*order_list)
        except KeyError:
            pass

        return products_query, sort_code

    @classmethod
    def _prepare_sorting_links(
            cls, request_url, sort_code, sort_dir):
        """Подготовка ссылок для сортировки товаров на странице

        :param request_url: исходный запрос
        :param sort_code: строка с кодом сортировки
        :param sort_dir: направление сортировки
        :return: список nametuple Sorting с информацией для сортировки
        """
        Sorting = namedtuple('Sorting', ['name', 'url', 'css_code'])

        def prepare_name(name, is_selected):
            """Подготовка названия сортировки для вывода на странице"""
            if is_selected:
                name = (f'{name}{"↑" if sort_dir == "asc" else "↓"}')
            return name

        sortings = []
        for code, sorting_dict in cls.sorting_dict.items():
            is_selected_code = code == sort_code
            current_sort_dir = get_sort_dir(sort_dir, is_selected_code)

            obj = Sorting(
                name=prepare_name(
                    sorting_dict['verbose_name'], is_selected_code),
                url=add_get_param_to_url(
                    request_url, dict(sort=code, sort_dir=current_sort_dir)),
                css_code=f'sorting {"selected" if is_selected_code else ""}'
            )
            sortings.append(obj)
        return sortings

    @classmethod
    def _get_sort_context(cls, request, sort_code, sort_dir):
        """Возвращает словарь с данными для сортировки"""

        context = dict(
            sort_code=sort_code,
            sort_dir=sort_dir,
            reversed_sort_dir=get_sort_dir(sort_dir, True),
            sortings=cls._prepare_sorting_links(
                request.get_full_path(), sort_code, sort_dir))
        return context

    def dispatch(self, request, *args, **kwargs):
        """Основная функция View"""

        # Применение сортировки
        sort_dir = get_sort_dir(request.GET.get('sort_dir'))
        products_query, sort_code = self._apply_sorting(
            self.queryset, request.GET.get('sort'), sort_dir)

        # Получение части запросов для отображения на текущей странице
        products = pagination_page(
            products_query, request.GET.get('page'), GOODS_ON_PAGE)

        context = prepare_products(products)
        context.update(self._get_sort_context(request, sort_code, sort_dir))

        return render(request, 'show_goods.html', context=context)


def add_url_view(request):
    data = {'form': UrlForm()}
    return render(request, 'add_url.html', context=data)


def add_product(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        message = add_url(url)
        return redirect(reverse('product:show_goods'))


def delete_product(request, product_id):
    if request.method == 'POST':
        message = delete_site(product_id)
        return redirect(reverse('product:show_goods'))
