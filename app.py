import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from wtforms import TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, SiteConfig, PortfolioCase, FAQ
from dotenv import load_dotenv
from flask import make_response


load_dotenv()
app = Flask(__name__)




@app.route('/robots.txt')
def robots():
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /login",
        f"Sitemap: https://your-domain.com/sitemap.xml"
    ]
    response = make_response("\n".join(lines))
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/sitemap.xml')
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>https://your-domain.com/</loc> 
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
      </url>
    </urlset>"""
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-super-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')

base_hash = 'scrypt:32768:8:1$nGRhWv7M4qraa4Bu$195dfd346b7a299b65991e313d08972923d272b2e2ed2fb10b159c3bd0b7a18908e5d99b09ddd90f2f418d52e1e6cd8392efbd50954213586932e6c52e5533a8'

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', base_hash)


db.init_app(app)

class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('logged_in') is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return super(SecureAdminIndexView, self).index()

class ConfigView(SecureModelView):
    can_create = False
    can_delete = False
    column_labels = {
        'first_name': 'Имя', 'last_name': 'Фамилия',
        'hero_title': 'Заголовок главного экрана', 'hero_subtitle': 'Подзаголовок',
        'about_title': 'Заголовок "Обо мне"', 'about_text': 'Текст "Обо мне"',
        'email': 'Почта', 'phone': 'Телефон', 'telegram': 'Telegram',
        'seo_title': 'SEO Title', 'seo_description': 'SEO Description',
        'seo_keywords': 'SEO Keywords', 'favicon': 'Favicon (Иконка сайта)'
    }
    form_overrides = {'about_text': TextAreaField}
    form_widget_args = {'about_text': {'rows': 5}}
    form_extra_fields = {
        'about_image': ImageUploadField('Фото автора', base_path=app.config['UPLOAD_FOLDER'], url_relative_path='uploads/'),
        'favicon': ImageUploadField('Favicon (.ico, .png)', base_path=app.config['UPLOAD_FOLDER'], url_relative_path='uploads/')
    }

class CaseView(SecureModelView):
    column_labels = {
        'title': 'Название проекта', 'description': 'Описание',
        'tech_stack': 'Стек технологий', 'image': 'Превью',
        'github_link': 'Ссылка на GitHub', 'live_link': 'Ссылка на проект (Demo)'
    }
    form_overrides = {'description': TextAreaField}
    form_widget_args = {'description': {'rows': 5}}
    form_extra_fields = {
        'image': ImageUploadField('Превью кейса', base_path=app.config['UPLOAD_FOLDER'], url_relative_path='uploads/')
    }

class FAQView(SecureModelView):
    column_labels = {
        'question': 'Вопрос', 'answer': 'Ответ', 'sort_order': 'Порядок сортировки (цифра)'
    }
    column_default_sort = 'sort_order'
    form_overrides = {'answer': TextAreaField}
    form_widget_args = {'answer': {'rows': 3}}

admin = Admin(app, name='Управление Портфолио', template_mode='bootstrap4', index_view=SecureAdminIndexView())
admin.add_view(ConfigView(SiteConfig, db.session, name='Настройки сайта'))
admin.add_view(CaseView(PortfolioCase, db.session, name='Кейсы (Портфолио)'))
admin.add_view(FAQView(FAQ, db.session, name='FAQ'))


@app.route('/')
def index():
    config = SiteConfig.query.first() or SiteConfig()
    cases = PortfolioCase.query.all()
    faqs = FAQ.query.order_by(FAQ.sort_order).all()
    return render_template('index.html', config=config, cases=cases, faqs=faqs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(request.args.get('next') or '/admin/')
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

with app.app_context():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.create_all()
    try:
        if not SiteConfig.query.first():
            db.session.add(SiteConfig())
            db.session.commit()
    except Exception:
        db.session.rollback()

if __name__ == '__main__':
    is_debug = os.environ.get('DEBUG', '0') == '1'
    app.run(debug=is_debug, port=5000)
