from ext.admin.views.admin_model_view_lte import AdminModelViewLTE


class BaseModelViewLTE(AdminModelViewLTE):
    page_size: int = 50  # the number of entries to display on the list view
    can_export: bool = True
    can_view_details: bool = True
    edit_modal: bool = False
    create_modal: bool = False
    details_modal: bool = True