from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from config.settings.dev import DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('product/', include('product.urls')),
    path('parsing/', include('parsing.urls')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
