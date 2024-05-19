from flask import Blueprint, render_template
from flask_security import auth_required, permissions_accepted, current_user

blueprint_name = 'admin'
import_name = __name__
template_folder = 'templates'
url_prefix = '/admin'

blueprint = Blueprint(blueprint_name, import_name, template_folder=template_folder, url_prefix=url_prefix)

@blueprint.route('/')
@auth_required()
@permissions_accepted("admin")
def main_index():
    return render_template('admin_index.html.j2')
