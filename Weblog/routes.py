from flask import Flask, render_template, request, redirect, url_for, flash, abort
from Weblog import app
from Weblog.forms import RegistrationForm, LoginForm, UpdateProfile, PostForm
from Weblog.models import User, Post
from Weblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def home():
    posts = Post.query.all()
    print(posts)
    return render_template('home.html', form=posts)


@app.route('/post/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail.html', det_post=post)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
        new_user = User(username=reg_form.username.data, email=reg_form.email.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        flash('You register successfully.', 'success')
        return redirect(url_for('home'))
    else:
        print('not valid')
    return render_template('registration.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            # next_page = request.args.get('next')
            flash('You login successfully', 'success')
            return redirect(url_for('home'))
            # return redirect(next_page if next_page else url_for('home'))
        else:
            flash('Email or Password is wrong', 'danger')
    return render_template('login.html', form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('you logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    upfrm = UpdateProfile()
    if upfrm.validate_on_submit():
        current_user.email = upfrm.email.data
        current_user.username = upfrm.username.data
        db.session.commit()
        flash('your account update successfully', 'info')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        upfrm.email.data = current_user.email
        upfrm.username.data = current_user.username
    return render_template('profile.html', form=upfrm)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def newpost():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, content=post_form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New post updated successfully', 'info')
        return redirect(url_for('home'))
    return render_template('post.html', form=post_form)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'info')
        return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.user:
        abort(403)
    upform = PostForm()
    if upform.validate_on_submit():
        post.title = upform.title.data
        post.content = upform.content.data
        db.session.commit()
        flash('Post successfully updated', 'info')
        return redirect(url_for('detail', post_id=post.id))
    elif request.method == 'GET':
        upform.title.data = post.title
        upform.content.data = post.content
        return render_template('update.html', form=upform)
