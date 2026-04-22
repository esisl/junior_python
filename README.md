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

Проектируем


| Требование ТЗ | Как реализуем |
| Кастомная аутентификация | Свои эндпоинты /api/auth/login/, /api/auth/register/ с ручной валидацией, хешированием через make_password(), выдачей токена |
| Кастомная авторизация | Таблицы Role, Resource, Action, PermissionRule + middleware для проверки |
| Мягкое удаление | Поле is_active + переопределение delete() + кастомный UserManager |
| Демонстрация правил | Админские эндпоинты /api/admin/permissions/ для CRUD правил |

| User | |
| Id (PK) | |
| Email (PK) | |
| password_hash | |
| first_name | |
| last_name | |
| patronymic | |
| role_id (FK) | |
| is_active (bool) | мягкое удаление |
| is_admin (bool) | флаг для упрощения |
| created_at | |
| updated_at | |
| deleted_at | для аудита |

1:1 через role_id 

| Role | |
| id (PK) | |
| name (UK) | "admin", "manager", "user" |
| description | |

1:N

| PermissionRule | |
| id (PK) | |
| role_id (FK) | |
| resource (str) | "article", "report", "user_profile" |
| action (str) | "create", "read", "update", "delete", "list" |
| allowed (bool) | |

| Token | |
| key (PK, str) | |
| user_id (FK) | User |
| created_at | | 
| is_revoked (bool) | принудительный логаут |
