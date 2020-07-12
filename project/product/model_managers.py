from django.db import models
from django.db.models import OuterRef, Subquery


class ProductPriceManager(models.Manager):
    """Менеджер для модели продукта, который добавляет в запрос поле
    current_price и price_date, т.е. текущую цену продукта и дату получения
    цены
    """

    def get_queryset(self):
        from product.models import Price

        price_subquery = Price.objects.filter(
            product_id=OuterRef('id')).order_by('-created')
        return super(ProductPriceManager, self).get_queryset().annotate(
            current_price=Subquery(price_subquery.values('price')[:1]),
            price_date=Subquery(price_subquery.values('created')[:1]))