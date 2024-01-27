from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product


# Create your views here.

class ProductListView(ListView):
    model = Product
    paginate_by = 2
    template_name = "catalog/home.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/products.html"


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('catalog:index')

    def form_invalid(self, form):
        return HttpResponse('Unsuccess')


def contacts(request):
    return render(request, 'catalog/contacts.html')




