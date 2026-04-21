from rest_framework import generics
from apps.rbac.models import PermissionRule
from apps.rbac.serializers import PermissionRuleSerializer
from apps.rbac.permissions import IsAdminUser

class PermissionRuleListCreateView(generics.ListCreateAPIView):
    queryset = PermissionRule.objects.select_related('role')
    serializer_class = PermissionRuleSerializer
    permission_classes = [IsAdminUser]

class PermissionRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PermissionRule.objects.select_related('role')
    serializer_class = PermissionRuleSerializer
    permission_classes = [IsAdminUser]