from django.urls import path

from . import views

app_name = "map"

urlpatterns = [
    path("", views.search, name="search"),
    path("detail/", views.search_detail, name="search_detail"),
    path("result/", views.search_result, name="search_result"),
    path('send_location/', views.receive_location, name='send_location'),
    path('get_location/', views.get_location, name='get_location'),
]