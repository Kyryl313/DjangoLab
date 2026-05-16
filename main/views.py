from django.shortcuts import render, get_object_or_404, redirect
from main.models import Category, Dish, Review, Subscriber, Order, OrderItem
from django.db.models import Avg
def home(request):
    categories = Category.objects.all().order_by('order')

    dishes = Dish.objects.all().order_by('category__order', 'name')
    cart = request.session.get('cart', {})

    cart_count = sum(cart.values())

    if request.method == "POST":

        email = request.POST.get('email')

        if email:
            Subscriber.objects.get_or_create(
                email=email
            )
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            Subscriber.objects.get_or_create(email=email)

            return redirect("home")
    return render(request, "main/home.html", {
        "categories": categories,
        "dishes": dishes,
        "title": "Меню",
        "selected_category": None,
        "cart_count": cart_count,

    })


def dish_detail(request, dish_id):

    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == "POST":

        rating = request.POST.get("rating")

        if rating:

            session_key = request.session.session_key

            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            Review.objects.update_or_create(
                dish=dish,
                session_key=session_key,
                defaults={"rating": int(rating)}
            )

            return redirect("dish_detail", dish_id=dish.id)

    average_rating = dish.reviews.aggregate(Avg("rating"))["rating__avg"]

    return render(request, "main/dish_detail.html", {
        "dish": dish,
        "average_rating": average_rating,
        "cart_count": sum(request.session.get("cart", {}).values()),
    })
def category_view(request, category_id):
    categories = Category.objects.all().order_by('order')

    category = get_object_or_404(Category, id=category_id)
    cart = request.session.get('cart', {})

    cart_count = sum(cart.values())
    dishes = Dish.objects.filter(
        category=category
    ).order_by('name')

    return render(request, "main/home.html", {
        "categories": categories,
        "dishes": dishes,
        "title": category.name,
        "selected_category": category,
        "cart_count": cart_count,
    })
def add_to_cart(request, dish_id):

    cart = request.session.get('cart', {})

    dish_id = str(dish_id)

    if dish_id in cart:
        cart[dish_id] += 1
    else:
        cart[dish_id] = 1

    request.session['cart'] = cart

    return redirect('cart')

def cart_view(request):

    cart = request.session.get('cart', {})

    cart_items = []

    total = 0

    for dish_id, quantity in cart.items():

        dish = Dish.objects.get(id=dish_id)

        item_total = dish.price * quantity

        total += item_total

        cart_items.append({
            'dish': dish,
            'quantity': quantity,
            'item_total': item_total
        })

    cart_count = sum(cart.values())

    return render(request, "main/cart.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": cart_count,
        "categories": Category.objects.all()
    })

def remove_from_cart(request, dish_id):

    cart = request.session.get('cart', {})

    dish_id = str(dish_id)

    if dish_id in cart:

        del cart[dish_id]

    request.session['cart'] = cart

    return redirect('cart')

def clear_cart(request):

    request.session['cart'] = {}

    return redirect('cart')

def update_cart(request, dish_id):

    if request.method == "POST":

        cart = request.session.get('cart', {})

        dish_id = str(dish_id)

        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart.pop(dish_id, None)
        else:
            cart[dish_id] = quantity

        request.session['cart'] = cart

    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0

    for dish_id, quantity in cart.items():
        dish = Dish.objects.get(id=dish_id)
        item_total = dish.price * quantity
        total += item_total

        cart_items.append({
            'dish': dish,
            'quantity': quantity,
            'item_total': item_total
        })

    if request.method == "POST":
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_price=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=item['dish'],
                quantity=item['quantity'],
                price=item['dish'].price
            )

        request.session['cart'] = {}

        return redirect('home')

    return render(request, "main/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": sum(cart.values()),
        "categories": Category.objects.all()
    })