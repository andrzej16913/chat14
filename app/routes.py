from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db, rooms
from app.forms import LoginForm, RegisterForm
from app.models import User, Room, Post


@app.route('/room/<name>')
@login_required
def room(name):
    room = db.session.execute(db.select(Room).filter_by(name='/{}'.format(name))).scalar_one_or_none()
    if room:
        posts = db.session.execute(db.select(Post).filter_by(room_id=room.id)).scalars().all()
        return render_template('session.html', title='Room - ' + name, namespace=name, posts=posts)
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration was succesful!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html', title='Start page', rooms=rooms)

