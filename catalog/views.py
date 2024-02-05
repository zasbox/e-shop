from django.db.models import Model
from django.forms import modelformset_factory, HiddenInput, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView

from catalog.forms import ProductForm, VersionForm, VersionFormSet
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

    def form_invalid(self, form):
        return redirect(reverse('catalog:index'))


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    exclude = ('created_at', 'modificated_at',)
    success_url = reverse_lazy('catalog:index')


def contacts(request):
    return render(request, 'catalog/contacts.html')


def manage_versions(request, fk):
    version_formset = modelformset_factory(Version, form=VersionForm, formset=VersionFormSet, extra=1, can_delete=True)
    if request.method == 'POST':
        pass
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


class VersionUpdateView(FormView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = modelformset_factory(Version, form=VersionForm, formset=VersionFormSet, extra=1, can_delete=True)
        if self.request.method == 'POST':
            formset = version_formset(self.request.POST)
            formset.extra_forms[0].fields['product'].initial = self.kwargs.get('fk')
            if formset.is_valid():
                formset.save()
        else:
            formset = version_formset(
                queryset=Version.objects.all().filter(product=self.kwargs.get('fk')))
            formset.extra_forms[0].fields['product'].initial = self.kwargs.get('fk')
        return {'formset': formset}

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):

        super().post(self, request, *args, **kwargs)
        form = self.get_form()
        print(form.is_valid())

        version_formset = modelformset_factory(Version, form=VersionForm, formset=VersionFormSet, extra=1, can_delete=True)
        formset = version_formset(self.request.POST)
        formset.extra_forms[0].fields['product'].initial = self.kwargs.get('fk')

        if formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
