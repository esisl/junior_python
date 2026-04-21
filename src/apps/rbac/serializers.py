from rest_framework import serializers
from apps.rbac.models import PermissionRule

class PermissionRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = PermissionRule
        fields = ['id', 'role', 'role_name', 'resource', 'action', 'allowed']