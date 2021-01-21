from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('customers/<str:pk_val>/', views.customers,name="customers"),
    path('products/',views.products,name="products"),
    path('ourProducts/', views.ourProducts,name="ourProducts"),
    path('create_order/',views.create_order,name="create_order"),
    path('update_order/<str:pk_val>/',views.update_order,name="update_order"),
    path('delete_order/<str:pk_val>/',views.delete_order,name="delete_order"),
    path('add_customer/',views.add_customer,name="add_customer"),
    path('update_customer/<str:pk_val>/',views.update_customer,name="update_customer"),
    path('place_orders/<str:pk_val>',views.place_orders,name="place_orders"),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('userProfile/',views.userProfile,name='userProfile'),
    path('account_setting/',views.accountSetting,name='account_setting'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    

]
