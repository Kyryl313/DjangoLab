from django.shortcuts import render, get_object_or_404
from main.models import Category, Dish
from django.shortcuts import render, get_object_or_404
from main.models import Dish, Category

def home(request):
    categories = Category.objects.all().order_by('order')

    dishes = Dish.objects.all().order_by('category__order', 'name')

    return render(request, "main/home.html", {
        "categories": categories,
        "dishes": dishes,
        "title": "Меню"
    })


def dish_detail(request, dish_id):
    categories = Category.objects.all()

    dish = get_object_or_404(Dish, id=dish_id)

    return render(request, "main/dish_detail.html", {
        "dish": dish,
        "categories": categories
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