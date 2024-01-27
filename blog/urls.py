from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('update/<str:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', ArticleDeleteView.as_view(), name='delete'),
    path('', ArticleListView.as_view(), name='list'),
    path('view/<str:slug>/', ArticleDetailView.as_view(), name='view'),
]
