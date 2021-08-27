from flask import request, render_template
from database import Topics, Publication, get_session
from typing import *


# THE HOME ROUTE FOR THE APP
def app_home():
    topic_number = -1

    topic_data: Dict = Topics.get_papers_per_topic()
    i = 1

    topic_counts: List[Dict] = []
    for topic in topic_data:
        topic_counts.append({'topic': topic.capitalize(), 'occurrences': topic_data[topic], 'ordinal': i})
        i += 1

    print(topic_counts)

    return render_template("topic_app/index.html.jinja2", topic_counts=topic_counts, topic_number=topic_number)


def topic_data(topic):
    topic_data: Dict = Topics.get_papers_per_topic()
    i = 1

    topic_counts: List[Dict] = []
    for t in topic_data:
        topic_counts.append({'topic': t.capitalize(), 'occurrences': topic_data[t], 'ordinal': i})
        i += 1

    session = get_session()
    topic = int(topic)

    publications: List[Publication] = []
    join = []
    if topic == 1:

        join = session.query(Publication).join(Publication.topics).filter(Topics.topic1 > 0).all()
    elif topic == 2:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic2 > 0).all()
    elif topic == 3:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic3 > 0).all()
    elif topic == 4:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic4 > 0).all()
    elif topic == 5:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic5 > 0).all()
    elif topic == 6:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic6 > 0).all()
    elif topic == 7:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic7 > 0).all()
    elif topic == 8:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic8 > 0).all()
    elif topic == 9:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic9 > 0).all()
    else:
        join = session.query(Publication).join(Publication.topics).filter(Topics.topic10 > 0).all()

    print(len(join))

    session.close()

    return render_template("topic_app/topics.html.jinja2", topic_counts=topic_counts, topic_number=int(topic), publications=join)

def publication_data(publication_id):
    topic_data: Dict = Topics.get_papers_per_topic()
    i = 1

    topic_counts: List[Dict] = []
    for t in topic_data:
        topic_counts.append({'topic': t.capitalize(), 'occurrences': topic_data[t], 'ordinal': i})
        i += 1


    publication_id = int(publication_id)

    session = get_session()
    publication: Publication = session.query(Publication).filter(Publication.id == publication_id).one()
    print(publication)
    session.close()
    
    return render_template("topic_app/publication.html.jinja2", topic_counts=topic_counts, topic_number=-1, publication=publication)