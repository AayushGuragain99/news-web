from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Post, Category
from .forms import RegistrationForm, LoginForm, PostForm
from . import db, bcrypt

main_bp = Blueprint('main', __name__)

# --- HOME PAGE ---
@main_bp.route("/")
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

# --- ADMIN DASHBOARD ---
@main_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    posts = Post.query.all()
    users = User.query.all()
    return render_template('admin_dashboard.html', posts=posts, users=users)

# --- PROFILE PAGE ---
@main_bp.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title='Account Profile')

# --- AUTHENTICATION ROUTES ---
@main_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# --- POST CRUD OPERATIONS ---
@main_bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # Pull categories from DB for the dropdown
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            content=form.content.data, 
            author=current_user, 
            category_id=form.category.data # Uses the ID from the dropdown
        )
        db.session.add(post)
        db.session.commit()
        flash('Your news post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form)

@main_bp.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@main_bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category_id
    return render_template('create_post.html', title='Update Post', form=form)

@main_bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'info')
    return redirect(url_for('main.index'))