from django.db import models

class PermissionRule(models.Model):
    role = models.ForeignKey('accounts.Role', on_delete=models.CASCADE, related_name='rules')
    resource = models.CharField(max_length=100, help_text="Например: 'article', 'report'")
    action = models.CharField(max_length=50, help_text="Например: 'create', 'read', 'update'")
    allowed = models.BooleanField(default=False)

    class Meta:
        db_table = 'rbac_permission_rule'
        # Уникальное правило на комбинацию роль+ресурс+действие
        unique_together = ('role', 'resource', 'action')

    def __str__(self):
        return f"{self.role.name} -> {'ALLOW' if self.allowed else 'DENY'} {self.action} {self.resource}"