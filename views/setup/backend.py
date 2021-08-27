from database import Publication, Author
from utilities import xmlparser
from typing import List, Dict
from sqlalchemy.orm import Session
from database import get_session
from flask import request

def import_xml_data():
    """
    A ROUTE TO IMPORT THE XML DATA FROM THE DATA FILES IN THE DATABASE.
    :return:
    """
    # PREVENT THIS FROM ACCIDENTALLY TRIGGERING
    if not request.args.get('override', None):
        return "Override required to perform this function again", 200

    publication_data: List[Dict]
    author_data: List[List[Dict]]

    publication_data, author_data = xmlparser.minidom_parse('./data/dblp-soc-papers.xml')

    publications: List[Publication] = []

    session: Session = get_session()
    print(f'processing publications')
    for i in range(0, len(publication_data)):
        if i % 200 == 0:
            print(f'Creating {i}th publication')
            session.commit()
        publication: Publication = Publication(**(publication_data[i]))
        publications.append(publication)
        session.add(publication)
    session.commit()
    print('publications saved')
    for i in range(0, len(publication_data)):
        if i % 200 == 0:
            print(f'handling {i}th list of authors')
            session.commit()

        for author_dict in author_data[i]:
            author_dict['publication_id'] = publications[i].id
            author: Author = Author(**author_dict)
            session.add(author)
    session.commit()
    print('authors saved')
    session.close()

    return "Check your console", 200
