from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    path('', views.main_app, name='main_app'),
    path('vid/<int:rtsp_url_id>/', views.mask_feed, name='mask_feed'),
]