from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cat-mec', views.ProductGroupsView.as_view(), name='product_groups'),
    path('about-us', views.AboutUsView.as_view(), name='about_us'),
]
