from flask import Blueprint, render_template, url_for, redirect, flash, request
from source.user.forms import BaseForm, LoginForm, GetItem, ItemForm, DiscoverManual
from source.user.models import User, Item
from flask_login import login_user, login_required, logout_user, current_user


user_blueprint = Blueprint('user',
                           __name__,
                           template_folder='templates/users')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = BaseForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=form.password.data,
                    experience=form.experience.data,
                    role_id=form.account_type.data)
        user.create(commit=True)
        return redirect(url_for('user.login'))
    return render_template("register.html", form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')

            if next is None:
                next = url_for('user.dashboard')

            return redirect(next)

    return render_template('login.html', form=form)


@user_blueprint.route('/discover_manual', methods=['GET', 'POST'])
def discover_manual():
    form = DiscoverManual()
    cur_user = current_user.get_id()
    return render_template("discover_manual.html", form=form, currebt_user=cur_user)


@user_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role_id == 1:
        return redirect('/admin')
    if current_user.role_id == 2:
        return render_template('user_dashboard.html')
    if current_user.role_id == 3:
        return render_template('creator_dashboard.html')
    if current_user.role_id == 4:
        return render_template('venue_dashboard.html')


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("User logged out")
    return redirect(url_for('base.index'))


@user_blueprint.route('/create_drinks', methods=['GET', 'POST'])
def create_drinks():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data,
                    ingredients=form.ingredients.data,
                    creator=current_user.username,
                    creator_id=current_user.id)
        item.create(commit=True)
        # user = User.find_by_email(current_user.email)
        # print(user.drinks)
        return redirect(url_for('user.your_drinks'))
    return render_template("create_item.html", form=form)


@user_blueprint.route('/read_drinks', methods=['GET', 'POST'])
def read_drinks():
    form = GetItem()
    all_items = Item.read_all()
    if form.validate_on_submit():
        item_id = form.id.data
        item = Item.read_one(item_id)
        return render_template('read_one_item.html', item=item)
    return render_template('read_all_items.html', form=form, all_items=all_items)


@user_blueprint.route('/your_drinks', methods=['GET', 'POST'])
def your_drinks():
    form = GetItem()
    user = User.find_by_email(current_user.email)
    drinks = user.all_drinks(user.id)
    print(type(drinks))
    # creators = user.all_creators(3)
    if form.validate_on_submit():
        for e in drinks:
            if form.id.data == e.id:
                item = Item.read_one(form.id.data)
                return render_template('read_one_item.html', item=item)
            else:
                render_template('read_all_items.html', form=form, all_items=drinks)
    return render_template('read_all_items.html', form=form, all_items=drinks)


@user_blueprint.route('/update_drinks', methods=['GET', 'POST'])
def update_drinks():
    form = GetItem()
    user = User.find_by_email(current_user.email)
    drinks = user.all_drinks(user.id)
    if form.validate_on_submit():
        for e in drinks:
            if form.id.data == e.id:
                return redirect(url_for('user.update_drink_data', id=form.id.data))
    return render_template('get_item.html', all_items=drinks, form=form)


@user_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update_drink_data(id):
    item = Item.read_one(id)
    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        ingredients = form.ingredients.data
        item.update(name=name,
                    ingredients=ingredients,
                    commit=True)
        return redirect(url_for('user.your_drinks'))
    return render_template('update_item.html', item=item, form=form)


@user_blueprint.route('/delete_drinks', methods=['GET', 'POST'])
def delete_drinks():
    form = GetItem()
    user = User.find_by_email(current_user.email)
    drinks = user.all_drinks(user.id)
    if form.validate_on_submit():
        for e in drinks:
            if form.id.data == e.id:
                item = Item.query.get(form.id.data)
                item.delete()
                return redirect(url_for('user.your_drinks'))
    return render_template('delete_item.html', all_items=drinks, form=form)


@user_blueprint.route('/read_creators', methods=['GET', 'POST'])
def read_creators():
    all_creators = User.query.filter_by(role_id=3)
    return render_template('read_all_creators.html', all_creators=all_creators)


@user_blueprint.route('/read_venues', methods=['GET', 'POST'])
def read_venues():
    all_venues = User.query.filter_by(role_id=4)
    return render_template('read_all_venues.html', all_venues=all_venues)
