from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
]