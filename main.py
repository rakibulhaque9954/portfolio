import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from forms import *
import os
from dotenv import load_dotenv

"""loading environment variables"""
load_dotenv()
username = os.environ.get("USERNAME")
pass_key = os.environ.get("PASS_KEY")

"""Initialising flask app"""
app = Flask(__name__)
ckeditor = CKEditor(app)

app.config['CKEDITOR_SERVE_LOCAL'] = True
Bootstrap(app)
app.config['SECRET_KEY'] = 'sdfsdfwefwefewf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects_portfolios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    id = 1
    username = username
    password = generate_password_hash(pass_key)

class MlProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    project_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f'Ml-project Name: {self.title}'


class WebProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    project_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f'Web-project Name: {self.title}'


class GameProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    project_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Game-project Name: {self.title}'


# new_ml_proj = GameProjects(
#     title='Game Test 3',
#     project_url='www.web2.com',
#     category='Game',
#     date='26-05-2020',
#     body='This is a test2 so we will do it soon',
# )
# with app.app_context():env
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        return User()
    return None


@app.route('/')
def home():
    print(username, pass_key)
    ml_results = MlProjects.query.all()
    web_results = WebProjects.query.all()
    game_results = GameProjects.query.all()
    return render_template('index.html', ml_projs=ml_results, web_projs=web_results, game_projs=game_results)



@app.route('/projects/ml/<index>', methods=['GET', 'POST'])
def ml_projects(index):
    project = MlProjects.query.get(index)
    return render_template('ml_projects.html', project=project, is_logged_in=current_user.is_authenticated)


@app.route('/projects/web/<index>')
def web_projects(index):
    project = WebProjects.query.get(index)
    return render_template('web_projects.html', project=project, is_logged_in=current_user.is_authenticated)


@app.route('/projects/games/<index>')
def game_projects(index):
    project = GameProjects.query.get(index)
    return render_template('game_projects.html', project=project, is_logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == User().username and check_password_hash(User().password, password):
            login_user(User())
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials', 'error')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out', 'success')
    return redirect(url_for('login'))

@app.route('/admin-dash')
@login_required
def dashboard():
    return render_template('admin_dash.html')


@app.route('/<catg>-projects')
@login_required
def all_projects(catg):
    if catg == 'web':
        results = WebProjects.query.all()
    elif catg == 'games':
        results = GameProjects.query.all()
    else:
        results = MlProjects.query.all()
    return render_template('all_projects.html', all_projs=results, category=catg)


@app.route('/projects/new-projects', methods=['GET', 'POST'])
@login_required
def new_project():
    form = CreatePostForm()
    time = datetime.datetime.now()
    if request.method == 'POST' and form.validate_on_submit():
        category = form.category.data
        title = form.title.data
        project_url = form.project_url.data
        date = str(time.strftime(f'%B %d, %Y'))
        body = form.body.data

        print(category)
        print(project_url)
        if category == 'ml':
            new_proj = MlProjects(title=title, category=category, project_url=project_url, date=date, body=body)
        elif category == 'web':
            new_proj = WebProjects(title=title, category=category, project_url=project_url, date=date, body=body)
        elif category == 'games':
            new_proj = GameProjects(title=title, category=category, project_url=project_url, date=date, body=body)
        else:
            pass

        db.session.add(new_proj)
        db.session.commit()
        return redirect(url_for('dashboard'))


    return render_template('add-project.html', form=form)


@app.route('/projects/edit-project', methods=['GET', 'POST'])
@login_required
def edit_project():
    category = request.args.get('catg')
    print(category)
    project_id = request.args.get('proj_id')
    time = datetime.datetime.now()
    try:
        if category == 'ml':
            result = MlProjects.query.get(project_id)
        elif category == 'web':
            result = WebProjects.query.get(project_id)
        elif category == 'games':
            result = GameProjects.query.get(project_id)
        else:
            raise ValueError('Invalid category')
    except Exception as e:
        # Handle the case when data is not found or an invalid category is provided
        # For example, you can display an error message or redirect the user to a different page.
        return f"Error: {e}"

    edit_form = CreatePostForm(title=result.title, category=category, project_url=result.project_url,
                               body=result.body) if result else CreatePostForm()
    if request.method == 'POST' and edit_form.validate_on_submit():
        new_category = edit_form.category.data
        if new_category != category:
            model_class = None
            if category == 'ml':
                model_class = MlProjects
            elif category == 'web':
                model_class = WebProjects
            elif category == 'games':
                model_class = GameProjects
            old_data = model_class.query.get(project_id)
            db.session.delete(old_data)
            db.session.commit()
            if new_category == 'ml':
                model_class = MlProjects
            elif new_category == 'web':
                model_class = WebProjects
            elif new_category == 'games':
                model_class = GameProjects
            new_project = model_class(title=edit_form.title.data, category=new_category,
                                      project_url=edit_form.project_url.data, body=edit_form.body.data,
                                      date=str(time.strftime(f'%B %d, %Y')))
            db.session.add(new_project)
            db.session.commit()
        result.category = new_category
        result.title = edit_form.title.data
        result.project_url = edit_form.project_url.data
        result.body = edit_form.body.data
        db.session.commit()

        return redirect(url_for('all_projects', catg=edit_form.category.data))
    return render_template('edit-project.html', form=edit_form)


@app.route('/delete-project')
@login_required
def delete_project():
    category = request.args.get('catg')
    project_id = request.args.get('proj_id')

    # Determine the appropriate model class based on the category
    model_class = None
    if category == 'ml':
        model_class = MlProjects
    elif category == 'web':
        model_class = WebProjects
    elif category == 'games':
        model_class = GameProjects

    # Delete the project if the model class is defined and project_id is valid
    if model_class and project_id:
        project_to_delete = model_class.query.get(project_id)
        if project_to_delete:
            db.session.delete(project_to_delete)
            db.session.commit()

    # Check if there are any posts remaining in the specific category
    has_posts = model_class.query.filter_by(category=category).count() > 0 if model_class else False

    # Redirect based on the presence of posts
    if has_posts:
        return redirect(url_for('all_projects', catg=category))
    return redirect(url_for('dashboard'))


@app.route('/search-results', methods=['POST'])
@login_required
def search():
    all_items = []
    results = []
    ml_items = MlProjects.query.all()
    web_items = WebProjects.query.all()
    game_items = GameProjects.query.all()
    all_items.append(ml_items)
    all_items.append(web_items)
    all_items.append(game_items)
    print(all_items)
    searched_term = request.form.get('searchTerm')
    print(searched_term)
    for category in all_items:
        for item in category:
            print(item.title)
            try:
                if searched_term.lower() in item.title.lower():
                    results.append(item)
            except TypeError:
                results = []
                pass
    print(results)
    return render_template('searched-items.html', results=results)

#
@app.route('/get-suggestions', methods=['POST'])
@login_required
def get_suggestions():
    all_items = []
    results = []
    ml_items = MlProjects.query.all()
    web_items = WebProjects.query.all()
    game_items = GameProjects.query.all()
    all_items.extend(ml_items)
    all_items.extend(web_items)
    all_items.extend(game_items)

    searched_term = request.json.get('searchTerm')

    for item in all_items:
        try:
            if searched_term.lower() in item.title.lower():
                results.append({'id': item.id, 'category': item.category, 'title': item.title})
        except TypeError:
            results = []
            pass

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

