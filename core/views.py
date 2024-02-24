
from django.shortcuts import render
from pets.models import Pet
from categories.models import Category

def home(request, category_slug = None):
    data = Pet.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Pet.objects.filter(category  = category)
    categories = Category.objects.all()
    return render(request, 'index.html', {'data' : data, 'category' : categories})
