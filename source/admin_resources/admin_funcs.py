from flask_admin.contrib.sqla import ModelView
from flask_user import current_user


class UserView(ModelView):
    def is_accessible(self):
        return current_user.has_roles('Admin')

    can_create = False
    can_delete = True
    can_edit = True
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', 'email', ]
    column_filters = ['account_type', 'experience', 'role']
    column_editable_list = ['username', 'email', 'experience', 'account_type', 'role', ]


class RoleView(ModelView):
    def is_accessible(self):
        return current_user.has_roles('Admin')

    can_create = True
    can_delete = True
    can_edit = True
    column_searchable_list = ['id', 'name']
    column_editable_list = ['id', 'name']


class UserRoleView(ModelView):
    def is_accessible(self):
        return current_user.has_roles('Admin')
    can_create = True
    can_delete = True
    can_edit = True
    column_list = ('id', 'user_id', 'role_id')
    column_searchable_list = ['id', 'user_id', 'role_id']
    # column_editable_list = ['id', 'user_id', 'role_id']
