from django.urls import path, re_path

from . import views

app_name = 'product'

urlpatterns = [
    path("all/", views.ProductListView.as_view(), name='product_list'),
    path("search/", views.SearchProductListView.as_view(), name='search_product'),
    re_path(r'^category/(?P<slug>[^/]+)/?$', views.CategoryProductListView.as_view(), name='category_products'),
    re_path(r'^mechanism/(?P<slug>[^/]+)/?$', views.MechanismProductListView.as_view(), name='mechanism_products'),
    re_path(r'^designer/(?P<slug>[^/]+)/?$', views.DesignerProductListView.as_view(), name='designer_products'),
    re_path(r'^publisher/(?P<slug>[^/]+)/?$', views.PublisherProductListView.as_view(), name='publisher_products'),
    re_path(r'(?P<slug>[^/]+)/?$', views.BoardGameDetailView.as_view(), name='board_game_detail'),
]
