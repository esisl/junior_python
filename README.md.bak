# Custom Auth & RBAC System

Учебный проект на Django + DRF. Реализована кастомная система аутентификации и разграничения прав доступа.

## 📐 Схема БД и правила доступа

### Структура
User (1) ──< Role >── (N) PermissionRule
│
├─ resource: str ("article", "report")
├─ action: str ("read", "create", "update", "delete")
└─ allowed: bool


### Алгоритм проверки `check_permission(user, resource, action)`
1. `user.is_active == False` → `DENY`
2. `user.is_admin == True` → `ALLOW` (суперпользователь)
3. `user.role == None` → `DENY`
4. Поиск правила: `PermissionRule.objects.filter(role=user.role, resource=..., action=...).first()`
5. Найдено → `return rule.allowed`
6. Не найдено → `DENY` (secure by default)

## 🚀 Запуск
```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python seed.py
docker compose exec web pytest --ds=config.settings apps/ -v

🔑 Тестовые пользователи
Email | Пароль | Роль | Доступ
admin@test.com | admin123 | admin | Полный доступ + CRUD правил
user@test.com | user123 | user | Только чтение статей

📝 API Endpoints
POST /api/auth/register/, /api/auth/login/, /api/auth/logout/
GET/PUT/DELETE /api/auth/profile/
GET/POST /api/admin/permissions/ (только admin)
GET /api/demo/articles/, POST /api/demo/articles/create/, GET /api/demo/reports/
Swagger UI: /api/docs/