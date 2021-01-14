from django.urls import path
from . import views

urlpatterns = [
    path('customers/<str:pk_val>/', views.customers,name="customers"),
    path('', views.home),
    path('products/',views.products),
    path('create_order/',views.create_order,name="create_order"),
    path('update_order/<str:pk_val>/',views.update_order,name="update_order"),
    path('delete_order/<str:pk_val>/',views.delete_order,name="delete_order"),
    path('add_customer/',views.add_customer,name="add_customer"),
    path('update_customer/<str:pk_val>/',views.update_customer,name="update_customer"),
    path('place_orders/<str:pk_val>',views.place_orders,name="place_orders"),
]
