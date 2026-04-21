from django.urls import path
from apps.rbac.views import PermissionRuleListCreateView, PermissionRuleDetailView

urlpatterns = [
    path('admin/permissions/', PermissionRuleListCreateView.as_view(), name='rule-list'),
    path('admin/permissions/<int:pk>/', PermissionRuleDetailView.as_view(), name='rule-detail'),
]