# src/apps/demo/urls.py
from django.urls import path
from apps.demo.views import ArticleListView, ArticleDetailView, ArticleCreateView, ReportListView

urlpatterns = [
    # GET /api/demo/articles/ -> список
    path('demo/articles/', ArticleListView.as_view(), name='article-list'),
    
    # POST /api/demo/articles/create/ -> создание (явный путь, чтобы не конфликтовать с list)
    path('demo/articles/create/', ArticleCreateView.as_view(), name='article-create'),
    
    # GET /api/demo/articles/<id>/ -> детальная
    path('demo/articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    
    # GET /api/demo/reports/ -> отчёты
    path('demo/reports/', ReportListView.as_view(), name='report-list'),
]