
# Interactive Portfolio
    
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)
![HTML](https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000)
![CSS](https://img.shields.io/badge/CSS-639?logo=css&logoColor=fff)

[English](#english-version) | [Русский](#русская-версия)

-----

## English Version

A lightweight, dynamic, and containerized portfolio designed for backend developers. It features a custom administrative panel for real-time content management (projects, FAQ, settings) without the bloat of a heavy CMS.

### Core Logic

  * **Admin Dashboard:** Powered by `Flask-Admin` with custom session-based auth and `scrypt` hashing.
  * **SEO Engine:** Dynamic `robots.txt` and `sitemap.xml` generation that adapts to your current host automatically.
  * **Performance:** Zero-dependency frontend using Vanilla JS and CSS variables. Features `IntersectionObserver` for scroll-triggered animations.
  * **Auto-Provisioning:** The app initializes the SQLite database and default site configs on the first launch using Flask's application context.
  * **Production Stack:** Gunicorn as the WSGI server, Nginx for reverse proxying and static file serving.

### Tech Stack

  * **Backend:** Python 3.12, Flask, Flask-SQLAlchemy, Flask-Admin.
  * **Frontend:** HTML5, CSS3, Vanilla JS.
  * **Database:** SQLite.
  * **Infrastructure:** Docker, Nginx, Gunicorn.

### Local Development

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/vdneech/portfolio.git
    cd portfolio
    ```

2.  **Environment Setup:**

    ```bash
    cp .env.example .env
    ```

3.  **Spin up the containers:**

    ```bash
    docker-compose up --build -d
    ```

<!-- end list -->

  * **Website:** `http://localhost/`
  * **Admin Panel:** `http://localhost/admin/` (Default: `admin` / `admin`).

<!-- end list -->

4.  **Security & Deployment:**
    Change the `SECRET_KEY` and admin password before deploying. To generate a new `scrypt` hash for your password, run:
    ```bash
    docker exec -it portfolio_web python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your_new_password'))"
    ```

-----

## Русская версия

Легковесный сайт-портфолио. Включает в себя панель управления для быстрого редактирования проектов.

### Технические особенности

  * **Панель управления:** На базе `Flask-Admin` с сессионной авторизацией и хэшированием пароля `scrypt`.
  * **SEO:** Динамическая генерация `robots.txt` и `sitemap.xml`, адаптирующаяся под домен.
  * **Оптимизация:** Фронтенд на чистом JS и нативных CSS-переменных. Весит мало, скорость большая.
  * **Автоматизация базы:** Базовый конфиг создается автоматически при запуске.
  * **Стек для продакшена:** Связка gunicorn и nginx для запросов и раздачи статики.

### Стек технологий

  * **Бэкенд:** Python 3.12, Flask, Flask-SQLAlchemy, Flask-Admin.
  * **Фронтенд:** HTML5, CSS3, JavaScript.
  * **База данных:** SQLite.
  * **Инфраструктура:** Docker, nginx, gunicorn.

### Локальный запуск

1.  **Клонирование репозитория:**

    ```bash
    git clone https://github.com/vdneech/portfolio.git
    cd portfolio
    ```

2.  **Настройка окружения:**

    ```bash
    cp .env.example .env
    ```

3.  **Сборка и запуск:**

    ```bash
    docker-compose up --build -d
    ```

<!-- end list -->

  * **Сайт:** `http://localhost/`
  * **Админ-панель:** `http://localhost/admin/` (Логин: `admin` Пароль: `admin`).

<!-- end list -->

4.  **Безопасность:**
    При деплое обязательно смените `SECRET_KEY` и пароль. Сгенерировать новый хеш пароля можно после запуска контейнера командой:
    ```bash
    docker exec -it portfolio_web python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('ваш_пароль'))"
    ```