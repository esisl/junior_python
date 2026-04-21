import secrets
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Хеширование средствами Django
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'rbac_role'
        verbose_name = 'Role'

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    patronymic = models.CharField(max_length=100, blank=True)
    
    # 1 пользователь = 1 роль. Если роль удалена - NULL (доступ запрещён)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts_user'

    def __str__(self):
        return self.email

    def soft_delete(self):
        """Мягкое удаление по ТЗ"""
        self.is_active = False
        # Аннулируем все активные токены
        self.tokens.update(is_revoked=True)
        self.save()

    def has_perm(self, perm, obj=None):
        """Заглушка для совместимости с Django admin, не используем в API"""
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class Token(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    is_revoked = models.BooleanField(default=False)

    class Meta:
        db_table = 'accounts_token'
        indexes = [models.Index(fields=['user', 'is_revoked'])]

    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(48)

    @classmethod
    def create_for_user(cls, user):
        """Создаёт новый токен, инвалидируя предыдущие"""
        cls.objects.filter(user=user, is_revoked=False).update(is_revoked=True)
        return cls.objects.create(key=cls.generate_key(), user=user)

    def __str__(self):
        return f"Token for {self.user.email}"