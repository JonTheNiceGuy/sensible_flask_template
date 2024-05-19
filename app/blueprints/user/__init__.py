from flask import Blueprint, render_template
from flask_security import auth_required, permissions_accepted, current_user

blueprint_name = 'user'
import_name = __name__
template_folder = 'templates'
url_prefix = '/user'

blueprint = Blueprint(blueprint_name, import_name, template_folder=template_folder, url_prefix=url_prefix)

@blueprint.route('/')
@auth_required()
@permissions_accepted("user-read")
def main_index():
    return render_template('user_index.html.j2')
