from django.urls import path
from . import views
from .views import potato_view, tomato_view

urlpatterns = [
    path("", views.index, name="index"),
    path('potato/',potato_view,name='potato'),
    path('tomato/', tomato_view,name='tomato'),
    path('weather/', views.weather, name='weather'),
    path('check-ip/', views.check_ip, name='check_ip'),
    path('upload/', views.upload_file, name='upload_file'),
]
