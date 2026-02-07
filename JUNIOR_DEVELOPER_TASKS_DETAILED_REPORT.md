# Детальный план доработки проекта Orkestrator Bot до продакшн версии

## Текущее состояние системы

### ✅ Достигнутые результаты
1. **Система развернута на сервере 192.168.88.170**
   - Backend работает на порту 8001 через uvicorn
   - PostgreSQL в Docker контейнере на порту 5433
   - Фронтенд обслуживается через FastAPI статические файлы

2. **Работающие компоненты**
   - Регистрация пользователей (`POST /api/auth/register`)
   - Авторизация (`POST /api/auth/login`)
   - JWT аутентификация
   - Middleware для защиты эндпоинтов
   - База данных с миграциями

3. **Инфраструктура**
   - SSH доступ настроен
   - Скрипт запуска `start_backend.sh`
   - Виртуальное окружение Python

### ❌ Критические проблемы (требуют немедленного решения)

#### 1. Проблемы с аутентификацией и middleware
- **Проблема**: Middleware неправильно извлекает user_id из токена
- **Симптомы**: Защищенные эндпоинты возвращают 401 даже с валидным токеном
- **Файлы для исправления**:
  - `dashboard/backend/middleware.py` - логика извлечения user_id
  - `dashboard/backend/auth.py` - проверка токенов
  - `dashboard/backend/app_auth.py` - генерация токенов

#### 2. Отсутствующие модули
- **app_auth** - требуется полная реализация с поддержкой refresh токенов
- **project_tree_api** - API для работы с деревом проектов
- **project_hierarchy_api** - API для иерархии проектов

#### 3. Проблемы с импортами Python
- **Циклические зависимости** между моделями SQLAlchemy
- **Относительные импорты** вызывают ошибки
- **Отсутствующие зависимости** (email-validator)

#### 4. Фронтенд не полностью интегрирован
- **Статические файлы** обслуживаются, но React приложение может не работать корректно
- **API вызовы** могут не соответствовать ожиданиям фронтенда
- **Маршрутизация** SPA требует настройки

## Детальный план задач для Junior разработчиков (4 недели)

### Неделя 1: Критические исправления и базовая функциональность

#### Задача 1.1: Исправить middleware аутентификации
**Срок**: 2 дня
**Файлы**:
- `dashboard/backend/middleware.py`
- `dashboard/backend/auth.py`
- `dashboard/backend/app_auth.py`

**Шаги**:
1. Проанализировать формат JWT токена (payload структура)
2. Исправить извлечение user_id в middleware
3. Добавить логирование для отладки
4. Протестировать с Postman/curl

**Критерии успеха**:
- `GET /api/projects` возвращает 200 с валидным токеном
- `GET /api/teams` возвращает 200 с валидным токеном
- Неавторизованные запросы возвращают 401

#### Задача 1.2: Создать недостающие модули
**Срок**: 3 дня
**Модули**:
- `app_auth.py` - полная реализация
- `project_tree_api.py` - базовый CRUD для деревьев
- `project_hierarchy_api.py` - управление иерархией

**Шаги**:
1. Создать `app_auth.py` с поддержкой:
   - Регистрации с валидацией email
   - Логина с проверкой пароля
   - Refresh токенов
   - Выхода (инвалидация токенов)
2. Создать `project_tree_api.py`:
   - CRUD операции для проектов
   - Валидация данных
   - Привязка к пользователю
3. Создать `project_hierarchy_api.py`:
   - Создание иерархии проектов
   - Перемещение между ветками
   - Рекурсивное получение дерева

#### Задача 1.3: Исправить импорты и зависимости
**Срок**: 2 дня
**Файлы**: Все файлы бекенда

**Шаги**:
1. Установить недостающие зависимости:
   ```bash
   pip install email-validator
   pip install python-multipart
   ```
2. Исправить циклические импорты в моделях
3. Заменить относительные импорты на абсолютные
4. Создать `requirements.txt` с полным списком зависимостей

### Неделя 2: Восстановление полного workflow

#### Задача 2.1: Настроить полную аутентификацию
**Срок**: 2 дня
**Функциональность**:
- Регистрация с подтверждением email
- Вход с запоминанием сессии
- Восстановление пароля
- Роли пользователей (user, admin)

**Шаги**:
1. Добавить модель Role в БД
2. Реализовать middleware для проверки ролей
3. Создать эндпоинты для админ-панели
4. Добавить логаут с инвалидацией токена

#### Задача 2.2: Реализовать CRUD для проектов
**Срок**: 3 дня
**Эндпоинты**:
- `GET /api/projects` - список проектов
- `POST /api/projects` - создание проекта
- `GET /api/projects/{id}` - получение проекта
- `PUT /api/projects/{id}` - обновление проекта
- `DELETE /api/projects/{id}` - удаление проекта

**Модели**:
- Project (id, name, description, user_id, created_at, updated_at)
- ProjectMember (project_id, user_id, role)
- ProjectFile (project_id, filename, path, size)

#### Задача 2.3: Интегрировать фронтенд с бекендом
**Срок**: 2 дня
**Интеграция**:
1. Настроить CORS для фронтенда
2. Создать API клиент на фронтенде
3. Реализовать обработку ошибок
4. Добавить индикаторы загрузки

### Неделя 3: UI/UX и соответствие ТЗ

#### Задача 3.1: Привести UI в соответствие с макетами
**Срок**: 3 дня
**Макеты**:
- `gpt_bot_ii.html` - интерфейс пользователя
- `admin_full.html` - админ-панель

**Шаги**:
1. Сравнить текущий UI с макетами
2. Исправить расхождения в верстке
3. Добавить недостающие компоненты
4. Настроить адаптивность

#### Задача 3.2: Реализовать недостающие функции из ТЗ
**Срок**: 2 дня
**Функции**:
- Управление командой проекта
- Система уведомлений
- Экспорт/импорт данных
- История изменений

#### Задача 3.3: Проверить выполнение всех задач
**Срок**: 2 дня
**Документ**: `Задачи.md`

**Шаги**:
1. Создать чеклист выполненных задач
2. Отметить выполненные пункты
3. Создать план для невыполненных
4. Обновить документацию

### Неделя 4: Качество кода и оптимизация

#### Задача 4.1: Проверить соответствие стандартам кода
**Срок**: 2 дня
**Документ**: `PATTERNS_AND_STANDARDS.md`

**Проверки**:
- Стиль кода (PEP 8 для Python, ESLint для JS)
- Структура проекта
- Комментарии и документация
- Обработка ошибок

#### Задача 4.2: Добавить тесты
**Срок**: 3 дня
**Тесты**:
- Unit тесты для бекенда (pytest)
- Интеграционные тесты API
- E2E тесты для фронтенда (Cypress)
- Тесты производительности

**Шаги**:
1. Настроить pytest для бекенда
2. Создать тесты для аутентификации
3. Создать тесты для CRUD операций
4. Настроить CI/CD для запуска тестов

#### Задача 4.3: Оптимизировать производительность
**Срок**: 2 дня
**Оптимизации**:
- Кэширование запросов (Redis)
- Оптимизация SQL запросов
- Сжатие статических файлов
- Ленивая загрузка компонентов

## Технические детали реализации

### 1. Структура JWT токена
Токен должен содержать:
```json
{
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "role": "user",
  "type": "access",
  "exp": 1234567890,
  "iat": 1234567800
}
```

### 2. Модель User для БД
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
```

### 3. Middleware логика
```python
async def auth_middleware(request: Request, call_next):
    # Пропускаем публичные эндпоинты
    if request.url.path in PUBLIC_ENDPOINTS:
        return await call_next(request)
    
    # Извлекаем токен
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Not authenticated"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = auth_header.split(" ")[1]
    
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Проверяем тип токена
        if payload.get("type") != "access":
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token type"}
            )
        
        # Извлекаем user_id
        user_id = payload.get("sub")
        if not user_id:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token payload"}
            )
        
        # Добавляем user_id в request state
        request.state.user_id = user_id
        request.state.user_email = payload.get("email")
        request.state.user_role = payload.get("role", "user")
        
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Token expired"}
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token"}
        )
    
    return await call_next(request)
```

### 4. Эндпоинты для тестирования

#### Публичные эндпоинты (без аутентификации):
- `GET /` - фронтенд
- `POST /api/auth/register` - регистрация
- `POST /api/auth/login` - вход
- `POST /api/auth/refresh` - обновление токена
- `POST /api/auth/forgot-password` - восстановление пароля

#### Защищенные эндпоинты (требуют аутентификации):
- `GET /api/projects` - список проектов
- `POST /api/projects` - создание проекта
- `GET /api/projects/{id}` - получение проекта
- `PUT /api/projects/{id}` - обновление проекта
- `DELETE /api/projects/{id}` - удаление проекта
- `GET /api/teams` - список команд
- `GET /api/user/profile` - профиль пользователя
- `PUT /api/user/profile` - обновление профиля

### 5. Переменные окружения
Создать файл `.env`:
```bash
# Database
DATABASE_URL=postgresql://bot:bot@localhost:5433/orkestrator

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://192.168.88.170:8001

# Email (для отправки уведомлений)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
```

## Метрики успеха

### Критические (обязательные к выполнению):
1. ✅ Веб-интерфейс доступен по http://192.168.88.170:8001/
2. ✅ Пользователи могут регистрироваться и входить
3. ✅ Все API эндпоинты возвращают корректные ответы
4. ✅ БД подключена, миграции применены
5. ✅ AI провайдеры интегрированы (если есть в ТЗ)

### Желательные (целевые):
1. 100% соответствие ТЗ
2. Все задачи из `Задачи.md` выполнены
3. UI полностью соответствует макетам
4. Код соответствует стандартам из `PATTERNS_AND_STANDARDS.md`
5. Написаны тесты с покрытием >80%
6. Система стабильно работает 24/7

## Рекомендации по процессу разработки

### Для Junior разработчиков:
1. **Ежедневные стендапы** - обсуждать прогресс и проблемы
2. **Code review** - все пулл-реквесты должны проходить ревью
3. **Тестирование** - писать тесты перед реализацией функциональности
4. **Документация** - обновлять документацию параллельно с кодом
5. **Версионирование** - использовать семантическое версионирование

### Для менеджмента:
1. **Контрольные точки** - проверять прогресс каждую неделю
2. **Мониторинг метрик** - отслеживать выполнение критических метрик
3. **Ресурсы** - обеспечить 2-3 junior разработчиков на 4 недели
4. **Инфраструктура** - предоставить доступ к тестовому окружению

## Ссылки и ресурсы

### Репозиторий:
- Основной: https://git.dipal.ru/av/orkestrator-bot
- Ветка с текущими изменениями: `merge-configs-to-main-2026-01-19`

### Документация:
- `ТЗ_full.txt` - полное техническое задание
- `PATTERNS_AND_STANDARDS.md` - стандарты кода
- `Задачи.md` - список задач
- `COMPLIANCE_ANALYSIS_REPORT.md` - анализ соответствия ТЗ

### Макеты:
- `gpt_bot_ii.html` - интерфейс пользователя
- `admin_full.html` - админ-панель

### Сервер:
- Адрес: 192.168.88.170:8001
- SSH: `av@192.168.88.170` (пароль: PoI456ZxC)
- БД: PostgreSQL на порту 5433 (пользователь: bot, пароль: bot)

## Заключение

Проект Orkestrator Bot находится на 65% готовности. При наличии 2-3 junior разработчиков и соблюдении данного плана, система может быть доведена до продакшн-готовности за 4 недели.

**Приоритеты**:
1. Исправить middleware аутентификации
2. Создать недостающие модули
3. Настроить полный workflow
4. Привести UI в соответствие с макетами
5. Добавить тесты и оптимизировать код

**Следующие шаги**: Начать с Недели 1, задачи 1.1 (исправление middleware).