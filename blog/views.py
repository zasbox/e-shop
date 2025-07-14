from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article
from blog.utils import EmailThread


class ArticleCreateView(UserPassesTestMixin, CreateView):
    model = Article
    fields = ('title', 'text', 'preview', 'is_published')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name="content_manager").exists()

    def handle_no_permission(self):
        return render(request=self.request, template_name='catalog/no_permissions.html')


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'text', 'preview', 'is_published')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('slug')])

    def test_func(self):
        return self.request.user.groups.filter(name="content_manager").exists()

    def handle_no_permission(self):
        return render(request=self.request, template_name='catalog/no_permissions.html')


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        return self.request.user.groups.filter(name="content_manager").exists()

    def handle_no_permission(self):
        return render(request=self.request, template_name='catalog/no_permissions.html')


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        if self.object.view_count == 100:
            EmailThread().start()
        return self.object
