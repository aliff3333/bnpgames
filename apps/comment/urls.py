from django.urls import path

from . import views

app_name = 'comment'

urlpatterns = [
    path('review/list-add/<int:product>', views.ReviewView.as_view(), name='review_list'),
]
