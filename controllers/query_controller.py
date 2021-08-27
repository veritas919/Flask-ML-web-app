from flask import Blueprint
import views
import queries

controller = Blueprint(name='query_controller', import_name='query_controller', url_prefix='/query')

controller.add_url_rule('/coauthors', view_func=views.queries.frontend.coauthors, methods=['GET'])
controller.add_url_rule('/paper-metadata', view_func=views.queries.frontend.paper_metadata, methods=['GET'])
controller.add_url_rule('/journal-metadata', view_func=views.queries.frontend.journal_metadata, methods=['GET'])
controller.add_url_rule('/conference-paper-metadata', view_func=views.queries.frontend.conference_paper_metadata, methods=['GET'])
controller.add_url_rule('/sose-papers', view_func=views.queries.frontend.bonus_query_2_1, methods=['GET'])
controller.add_url_rule('/researcher-paper-titles', view_func=views.queries.frontend.bonus_query_2_2, methods=['GET'])
controller.add_url_rule('/authors-with-more-than-ten', view_func=views.queries.frontend.bonus_query_2_3, methods=['GET'])
controller.add_url_rule('/publication-metadata-xquery', view_func=views.queries.frontend.bonus_query_2_4, methods=['GET'])

controller.add_url_rule('/researchers-articles-metadata', view_func=views.queries.frontend.lab2_mashup1, methods=['GET'])
controller.add_url_rule('/productive-authors-coauthors', view_func=views.queries.frontend.lab2_mashup2, methods=['GET'])