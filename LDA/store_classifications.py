import json
from typing import *
from sqlalchemy import or_
from database import *
from database.types import Topics
import sqlalchemy.orm

def load_json_from_file() -> List:
    with open("./LDA/topic_distribution.json") as f:
        data = f.read()

    j: Dict = json.loads(data)
    return j

def run():
    topic_data: List = load_json_from_file()
    session = get_session()

    i: int = 0
    topics: List[Topics] = []
    for datum in topic_data:
        print(f'processing datum {i} of {len(topic_data)}' )
        i += 1
        title = datum['title']
        publication: Publication
        try:
            publication = session.query(Publication).filter((or_(Publication.title == title, Publication.title.like(f'%{title}%')))).first()
        except sqlalchemy.orm.exc.NoResultFound:
            print('skipping!')
            continue
        if not publication:
            print('skipping!')
            continue
        topic: Topics = Topics(publication_id=publication.id or 0,
                               topic1=datum.get('0', 0),
                               topic2=datum.get('1', 0),
                               topic3=datum.get('2', 0),
                               topic4=datum.get('3', 0),
                               topic5=datum.get('4', 0),
                               topic6=datum.get('5', 0),
                               topic7=datum.get('6', 0),
                               topic8=datum.get('7', 0),
                               topic9=datum.get('8', 0),
                               topic10=datum.get('9', 0),
                                predicted_topic=datum.get('predicted class'))
        topics.append(topic)
    print(f'Got topic data for {len(topics)} publications')
    session.add_all(topics)
    session.commit()
    session.close()