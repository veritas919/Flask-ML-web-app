from flask import Blueprint
import views

controller = Blueprint(name='topic_app_controller', import_name='topic_app_controller', url_prefix='/app')

# APP ROUTES
controller.add_url_rule("/", view_func=views.topic_app.frontend.app_home, methods=['GET'])
controller.add_url_rule("/topic/<topic>", view_func=views.topic_app.frontend.topic_data, methods=['GET'])
controller.add_url_rule("/publication/<publication_id>", view_func=views.topic_app.frontend.publication_data, methods=['GET'])

# API ROUTES
controller.add_url_rule("/api/publication/<publication_id>", view_func=views.topic_app.backend.get_publication, methods=['GET'])
controller.add_url_rule("/api/topics/<publication_id>", view_func=views.topic_app.backend.get_topic, methods=['GET'])