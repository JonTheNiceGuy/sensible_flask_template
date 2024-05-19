from flask import Blueprint, render_template

blueprint_name = 'welcome'
import_name = __name__
template_folder = 'templates'
url_prefix = '/'

blueprint = Blueprint(blueprint_name, import_name, template_folder=template_folder, url_prefix=url_prefix)

@blueprint.route('/')
def main_index():
    return render_template('index.html.j2')
