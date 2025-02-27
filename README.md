# Blog API

Инструкция по настройке и запуску приложения Blog API

## Описание проекта

Blog API - это backend-приложение на FastAPI для управления постами в блоге. Использует SQLAlchemy, Redis для кэширования статистики (посты в день), Docker Compose и Poetry

## Переменные окружения

Создайте *.env* файл, например:
- DB_NAME=your_db_name
- DB_USER=your_db_user
- DB_PASS=your_db_password
- DB_HOST=localhost
- DB_PORT=5432
- REDIS_HOST=localhost
- REDIS_PORT=6379
- SECRET_KEY=your_secret_key
- ALGORITHM=HS256

## Запуск приложения
1. Склонируйте репозиторий и перейдите в директорию проекта:
```
git clone https://github.com/adrlksv/blog-api.git
cd blog-api
```
2. Запустите приложение:
```
docker-compose up --build
```

Приложение будет доступно по адресу *http://localhost:7000*


## API Эндпоинты

### Аутентификация (/auth)

*   **POST /auth/register**: Регистрация.
*   **POST /auth/login**: Логин, устанавливает куки refer_access_token, refer_refresh_token.
*   **POST /auth/refresh**: Обновление токена доступа (из куки refer_refresh_token), устанавливает куку refer_access_token.
*   **POST /auth/logout**: Выход (удаляет куки).
*   **GET /auth/me**: Информация о пользователе (требуется авторизации).

### Посты (/posts)

*   **GET /posts**: Все посты пользователя (требуется авторизации).
*   **GET /posts/{post_id}**: Пост по ID (требуется авторизации).
*   **POST /posts**: Создать пост (требуется авторизации).
*   **GET /posts/stats/posts**: Статистика по созданным постам текущего пользователя за сегодня (требуется авторизация)
