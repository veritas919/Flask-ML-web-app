from xml.dom import minidom
from utilities import xmlparser
from typing import List, Dict
import sqlalchemy.orm
import database

def parse_abstracts() -> Dict:

    dom = minidom.parse('data/dblp_abstract_dataset.xml')
    articles: List = dom.getElementsByTagName("article")
    article_abstracts: List = []

    inproceedings: List = dom.getElementsByTagName("inproceedings")
    inproceedings_abstracts: List = []

    # MAP TITLES TO ABSTRACTS
    map: Dict = {}

    # ADD ABSTRACTS
    for article in articles:
        title = xmlparser.get_child_tag_data(article, 'title')
        abstract = xmlparser.get_child_tag_data(article, 'abstract')
        map[title] = abstract


    for inproceeding in inproceedings:
        title = xmlparser.get_child_tag_data(inproceeding, 'title')
        abstract = xmlparser.get_child_tag_data(inproceeding, 'abstract')

        map[title] = abstract.rstrip().strip()

    print(len(map))
    return map

def update_publications():
    map = parse_abstracts()
    session: sqlalchemy.orm.Session = database.get_session()
    exceptions: int = 0
    successes: int = 0
    for publication in session.query(database.Publication).all():
        try:
            abstract = map[publication.title]
            publication.abstract = abstract
            successes += 1
        except KeyError as e:
            exceptions += 1
            print(f'Exception while trying to get title for publication {publication.id}: {e}')
    print(f'Exceptions: {exceptions}')
    print(f'Successes: {successes}')
    print(f'Map length: {len(map)}')
    session.commit()
    session.close()

    print("Finished")

def clean_data():
    session: sqlalchemy.orm.Session = database.get_session()
    for publication in session.query(database.Publication).all():
        publication.title = publication.title.strip().rstrip()

    session.commit()
    session.close()
