from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload/', views.upload_view, name='upload_view'),
    path('load-demo-data/', views.load_demo_data_view, name='load_demo_data'),
]