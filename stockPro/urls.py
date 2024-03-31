from django.urls import path
from . import views
app_name = 'stockPro' 

urlpatterns = [
    path('', views.enter_stock_data, name='enter_stock_data'),
    path('fetch_data/', views.fetch_stock_data, name='fetch_data'),
]