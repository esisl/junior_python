# src/apps/demo/urls.py
from django.urls import path
from apps.demo.views import ArticleListView, ArticleDetailView, ArticleCreateView, ReportListView

urlpatterns = [
    path('demo/articles/', ArticleListView.as_view(), name='article-list'),
    path('demo/articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('demo/articles/', ArticleCreateView.as_view(), name='article-create'),
    path('demo/reports/', ReportListView.as_view(), name='report-list'),
]