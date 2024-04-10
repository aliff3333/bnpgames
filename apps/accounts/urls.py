from django.urls import path, include
from . import views

app_name = "accounts"

address_patterns = [
    path('', views.AddressListCreationView.as_view(), name='add_list_address'),
    path('del/<int:pk>/', views.AddressDelete.as_view(), name='remove_address'),
    path('set-active/<int:pk>/', views.AddressSetActive.as_view(), name='set_active_address'),
]

urlpatterns = [
    path(
        'my-account/',
        include(
            [
                path('', views.UserProfileView.as_view(), name='user_profile'),
                path('factors/', views.UserOrdersView.as_view(), name='factors'),
                path('address/', include(address_patterns)),
            ]
        )
    ),
    path('logout/', views.CustomLogoutView.as_view(), name='account_logout'),
]
