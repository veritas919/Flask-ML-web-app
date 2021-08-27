from database import *
from sqlalchemy.orm import Session
import sqlalchemy.orm.exc as sqlalchemy_errors
from typing import *
from flask import jsonify


# METHOD TO GET A PUBLICATION GIVEN A PUBLICATION ID
def get_publication(publication_id: str):
    id: int = int(publication_id)

    try:
        session: Session = get_session()
        publication: Publication = session.query(Publication).filter(Publication.id == id).one()

        session.close()
        return jsonify(publication.as_dict())
    except sqlalchemy_errors.NoResultFound as e:
        return jsonify(error="Unable to find a publication with that id"), 404


# METHOD TO GET A TOPIC FOR A PUBLICATION GIVEN A PUBLICATION ID
def get_topic(publication_id: str):
    id: int = int(publication_id)

    try:
        session: Session = get_session()
        topics: Topics = session.query(Topics).filter(Topics.publication_id == id).first()
        session.close()

        if topics is None:
            return jsonify(error="Unable to find a topic listing with that id"), 404
        else:

            return jsonify(topics.as_dict())
    except sqlalchemy_errors.NoResultFound as e:
        return jsonify(error="Unable to find a topic listing with that id"), 404
