from flask import Blueprint
import views
import queries

controller = Blueprint(name='raw_controller', import_name='raw_controller', url_prefix='/raw')

controller.add_url_rule('/researchers-articles-metadata', view_func=views.queries.backend.lab2_mashup_1, methods=['GET'])
controller.add_url_rule('/productive-authors-coauthors', view_func=views.queries.backend.lab2_mashup_2, methods=['GET'])


controller.add_url_rule('/coauthors', view_func=views.queries.backend.coauthors, methods=['GET'])
controller.add_url_rule('/paper-metadata', view_func=views.queries.backend.paper_metadata, methods=['GET'])
controller.add_url_rule('/journal-metadata', view_func=views.queries.backend.journal_metadata, methods=['GET'])
controller.add_url_rule('/conference-paper-metadata', view_func=views.queries.backend.conference_paper_metadata, methods=['GET'])
controller.add_url_rule('/sose-papers', view_func=views.queries.backend.bonus_query_2_1, methods=['GET'])
controller.add_url_rule('/researcher-paper-titles', view_func=views.queries.backend.bonus_query_2_2, methods=['GET'])
controller.add_url_rule('/authors-with-more-than-ten', view_func=views.queries.backend.bonus_query_2_3, methods=['GET'])
controller.add_url_rule('/publication-metadata-xquery', view_func=views.queries.backend.bonus_query_2_4, methods=['GET'])