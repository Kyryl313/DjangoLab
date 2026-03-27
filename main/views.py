from django.shortcuts import render

def home(request):
    context = {
        "title": "Головна сторінка",
        "message": "Лаб3"
    }
    return render(request, "main/home.html", context)

def about(request):
    context = {
        "title": "Про нас",
        "message": "Сторінка про нас"
    }
    return render(request, "main/about.html", context)