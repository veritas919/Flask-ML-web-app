from flask import Blueprint
import views

controller = Blueprint(name='setup_controller', import_name='setup_controller', url_prefix='/setup')

controller.add_url_rule("/database", view_func=views.setup.backend.import_xml_data, methods=['GET', 'PUT'])