from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm, VersionInlineFormSet, VersionFormSet
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    template_name = "catalog/home.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        for product in queryset:
            version = product.version_set.all().filter(is_currency=True).first()
            product.version = version
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/products.html"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    exclude = ('created_at', 'modificated_at',)
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(parent_model=Product, model=Version, form=VersionForm,
                                                formset=VersionInlineFormSet, extra=1, can_delete=True)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    exclude = ('created_at', 'modificated_at',)
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(parent_model=Product, model=Version, form=VersionForm,
                                                formset=VersionInlineFormSet, extra=1, can_delete=True)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


def contacts(request):
    return render(request, 'catalog/contacts.html')


def manage_versions(request, fk):
    version_formset = modelformset_factory(Version, form=VersionForm, formset=VersionFormSet, extra=1, can_delete=True)
    if request.method == 'POST':
        formset = version_formset(request.POST)
        formset.extra_forms[0].fields['product'].initial = fk
        if formset.is_valid():
            formset.save()
            return redirect(reverse('catalog:index'))
    else:
        formset = version_formset(
            queryset=Version.objects.all().filter(product=fk))
        formset.extra_forms[0].fields['product'].initial = fk
    return render(request, "catalog/version_form.html", {'formset': formset})
