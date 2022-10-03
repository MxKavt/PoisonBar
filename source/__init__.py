from flask import Flask
from source.extensions import db, migrate, login_manager, admin
from flask_admin.menu import MenuLink
from source.user.models import User, Role, Item, ItemUsers
from source.admin_resources.admin_funcs import UserView, RoleView, UserRoleView, ItemView, ItemUsersView


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    admin.init_app(app)
    admin.add_view(UserView(User, db.session, category="Management", endpoint="users_"))
    admin.add_view(RoleView(Role, db.session, category="Management", endpoint="roles_"))
    admin.add_view(ItemView(Item, db.session, category="Management", endpoint="item_"))
    admin.add_view(ItemUsersView(ItemUsers, db.session, category="Management", endpoint="item_users_"))
    admin.add_link(MenuLink(name='Return to Home', url='/', ))


def register_blueprints(app):
    from source.user.views import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from source.front.views import base_blueprint
    app.register_blueprint(base_blueprint)



