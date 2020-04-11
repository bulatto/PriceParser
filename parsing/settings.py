import os

from config.settings import BASE_DIR


# Расположение изображений товаров
GOODS_IMAGE_PATH = os.path.join(BASE_DIR, "static", 'goods_images')
DEFAULT_IMG_PATH = os.path.join(GOODS_IMAGE_PATH, 'default.jpg')
