from flask import Blueprint, render_template, url_for, redirect
from source.user.forms import ItemForm, GetItem
from source.user.models import Item


item_blueprint = Blueprint('item',
                           __name__,
                           template_folder='templates/items')


@item_blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = ItemForm()

    if form.validate_on_submit():
        item = Item(name=form.name.data,
                    ingredients=form.ingredients.data)
        item.create(commit=True)
        return redirect(url_for('item.read_all'))
    return render_template("create_item.html", form=form)


@item_blueprint.route('/read_all', methods=['GET'])
def read_all():
    all_items = Item.read_all()
    return render_template('read_all_items.html', all_items=all_items)


@item_blueprint.route('/read_one', methods=['GET', 'POST'])
def read_one():
    form = GetItem()
    if form.validate_on_submit():
        item_id = form.id.data
        item = Item.read_one(item_id)
        return render_template('read_one_item.html', item=item)
    return render_template('get_item.html', form=form)


@item_blueprint.route('/update', methods=['GET', 'POST'])
def update():
    get_form = GetItem()
    all_items = Item.read_all()
    if get_form.validate_on_submit():
        return redirect(url_for('item.update_item', id=get_form.id.data))
    return render_template('get_item.html', all_items=all_items, form=get_form)


@item_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.read_one(id)
    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        ingredients = form.ingredients.data
        item.update(name=name,
                    ingredients=ingredients,
                    commit=True)
        return redirect(url_for('item.read_all'))
    return render_template('update_item.html', item=item, form=form)


@item_blueprint.route('/delete', methods=['GET', 'POST'])
def delete():
    form = GetItem()
    all_items = Item.read_all()
    if form.validate_on_submit():
        item_id = form.id.data
        item = Item.query.get(item_id)
        item.delete()
        return redirect(url_for('item.read_all'))
    return render_template('get_item.html', all_items=all_items, form=form)
