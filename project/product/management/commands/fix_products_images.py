from django.core.management import BaseCommand

from product.helpers import fix_photo_paths_in_products
from product.helpers import remove_unused_products_photo


class Command(BaseCommand):
    help = ('Очищает ненужные изображения товаров, обновляет поле с '
            'изображением у тех товаров, у которых поле photo_path непустое, '
            'но ссылается на несуществующий файл')

    def handle(self, *args, **options):
        print('Запущена команда для очистки ненужных фото и обновления '
              'некорректных полей с изображениями товаров')
        # Удаление неиспользуемых файлов из папки с фото товаров для удаления
        remove_unused_products_photo()
        # Исправление заполненных полей у продуктов, которые указывают на
        # несуществующий файл (для этих продуктов поле photo_path = None)
        fix_photo_paths_in_products()
