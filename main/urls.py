from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:dish_id>/',
     views.remove_from_cart,
     name='remove_from_cart'),
    path('clear-cart/',
     views.clear_cart,
     name='clear_cart'),
    path('update-cart/<int:dish_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
]