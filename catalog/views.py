from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView

from catalog.forms import ProductForm, VersionForm, VersionInlineFormSet, VersionFormSet
from catalog.models import Product, Version


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 4
    template_name = "catalog/home.html"
    login_url = reverse_lazy('users:login')

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        for product in queryset:
            version = product.version_set.all().filter(is_currency=True).first()
            product.version = version
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/products.html"
    login_url = reverse_lazy('users:login')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    exclude = ('created_at', 'modificated_at',)
    success_url = reverse_lazy('catalog:index')
    login_url = reverse_lazy('users:login')

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
            self.object = form.save()
            self.object.user = self.request.user
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    exclude = ('created_at', 'modificated_at',)
    success_url = reverse_lazy('catalog:index')
    login_url = reverse_lazy('users:login')

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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    login_url = reverse_lazy('users:login')


def contacts(request):
    return render(request, 'catalog/contacts.html')


@login_required
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


class VersionUpdateView(LoginRequiredMixin, FormView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy('catalog:index')
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = modelformset_factory(Version, form=VersionForm, formset=VersionFormSet, extra=1,
                                               can_delete=True)
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

        version_formset = modelformset_factory(Version, form=VersionForm, formset=VersionFormSet, extra=1,
                                               can_delete=True)
        formset = version_formset(self.request.POST)
        formset.extra_forms[0].fields['product'].initial = self.kwargs.get('fk')

        if formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
