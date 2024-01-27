from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product


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
        return redirect(reverse('catalog:index'))


def contacts(request):
    return render(request, 'catalog/contacts.html')




