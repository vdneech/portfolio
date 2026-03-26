from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SiteConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), default="Имя")
    last_name = db.Column(db.String(100), default="Фамилия")
    hero_title = db.Column(db.String(200), default="BACKEND-РАЗРАБОТЧИК")
    hero_subtitle = db.Column(db.String(200), default="Высокоскоростная инфраструктура под ключ.")
    about_title = db.Column(db.String(200), default="Обо мне")
    about_text = db.Column(db.Text, default="Текст о вашем опыте...")
    about_image = db.Column(db.String(200))
    email = db.Column(db.String(100), default="hello@example.com")
    phone = db.Column(db.String(50), default="+7 (999) 000-00-00")
    telegram = db.Column(db.String(100), default="@telegram")

    seo_title = db.Column(db.String(150), default="Портфолио Backend-разработчика")
    seo_description = db.Column(db.String(300), default="Персональный сайт разработчика. Проекты, услуги, контакты.")
    seo_keywords = db.Column(db.String(200), default="backend, developer, python, portfolio")
    favicon = db.Column(db.String(200))


class PortfolioCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))


    github_link = db.Column(db.String(300))
    live_link = db.Column(db.String(300))


class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0)