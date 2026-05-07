from django.shortcuts import render, get_object_or_404
from main.models import Category, Dish


def home(request):
    categories = Category.objects.all().order_by('order')

    dishes = Dish.objects.all().order_by('category__order', 'name')

    return render(request, "main/home.html", {
        "categories": categories,
        "dishes": dishes,
        "title": "Меню"
    })


def category_view(request, category_id):
    categories = Category.objects.all().order_by('order')

    category = get_object_or_404(Category, id=category_id)

    dishes = Dish.objects.filter(
        category=category
    ).order_by('name')

    return render(request, "main/home.html", {
        "categories": categories,
        "dishes": dishes,
        "title": category.name
    })