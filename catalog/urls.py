from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    manage_versions, VersionUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('contacts/', contacts, name='contacts'),
    # path('version/update/<int:fk>/', VersionUpdateView.as_view(), name='update_version'),
    path('version/update/<int:fk>/', manage_versions, name='update_version'),
]
