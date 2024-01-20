from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from catalog.forms import ProductForm
from catalog.models import Product, Category
from config import settings


# Create your views here.

def index(request):
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     phone = request.POST.get('phone')
    #     message = request.POST.get('message')
    #     print(f'{name}, {phone}, {message}')
    return product_list(request, 1)
    # product_list = Product.objects.all()
    # context = {
    #     'object_list': product_list,
    #     'page_list': range(1, product_list.count() // 2 + 1 + bool(product_list.count() % 2))
    # }
    # return render(request, 'catalog/home.html', context)


def contacts(request):
    return render(request, 'catalog/contacts.html')


def product_list(request, page=None):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        product_list = Product.objects.all()
        context = {
            'object_list': product_list,
        }
        return render(request, 'catalog/home.html', context)
    elif page is not None:
        begin = 2 * (page - 1)
        product_list = Product.objects.all()
        context = {
            'object_list': product_list[begin:begin + 2],
            'page_list': range(1, product_list.count() // 2 + 1 + bool(product_list.count() % 2))
        }
        return render(request, 'catalog/home.html', context)

    else:
        begin = 0
        if page is not None:
            begin = 2 * (page - 1) - 1
        category_list = Category.objects.all()[begin:]
        context = {
            'object_list': category_list,
        }
        return render(request, 'catalog/add_product.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'catalog/products.html', {'object': product})
