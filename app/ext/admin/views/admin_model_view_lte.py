from flask_admin.contrib.sqla import ModelView #type: ignore


class AdminModelViewLTE(ModelView):

    list_template: str = "flask-admin/model/list.html"
    create_template: str = "flask-admin/model/create.html"
    edit_template: str = "flask-admin/model/edit.html"
    details_template: str = "flask-admin/model/details.html"
    create_modal_template: str = "flask-admin/model/modals/create.html"
    edit_modal_template: str = "flask-admin/model/modals/edit.html"
    details_modal_template: str = "flask-admin/model/modals/details.html"