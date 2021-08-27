from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from .driver import get_session
from typing import List, Dict

Base = declarative_base()

"""
WORTH NOTING THAT I WOULD REALLY PREFER TO HAVE THE PUBLICATION AND AUTHOR CLASSES IN DIFFERENT FILES, BUT FOR SOME
REASON, SQLALCHEMY REALLY DOESN'T LIKE THAT, PROBABLY BECAUSE THEY'RE LINKED VIA A FOREIGN KEY. 
KINDA ANNOYING BUT GO FIGURE
"""


class Publication(Base):
    """
    THE CLASS CORRESPONDING TO THE PUBLICATIONS TABLE
    """

    __tablename__ = 'publications'

    id: int = Column(Integer, primary_key=True, nullable=False)
    type: str = Column(String(20), nullable=False)
    title: str = Column(String(400))
    abstract: str = Column(Text)
    booktitle: str = Column(String(400))
    pages: str = Column(String(400))
    year: int = Column(Integer)
    address: str = Column(String(400))
    journal: str = Column(String(400))
    volume: int = Column(Integer)
    number: int = Column(Integer)
    month: str = Column(String(16))
    url: str = Column(String(400))
    ee: str = Column(String(120))
    cdrom: str = Column(String(40))
    cite: str = Column(String(200))
    publisher: str = Column(String(100))
    note: str = Column(String(40))
    crossref: str = Column(String(100))
    isbn: str = Column(String(20))
    series: str = Column(String(40))
    school: str = Column(String(100))
    chapter: int = Column(String(Integer))
    publnr: str = Column(String(100))

    series_href: str = Column(String(40))
    mdate: str = Column(Date)  # POSSIBLE A DATETIME?
    key: str = Column(String(40))
    ee_type: str = Column(String(20))

    authors = relationship('Author', lazy='subquery')
    topics = relationship('Topics', lazy='joined', uselist=False)

    # presents row as dictionary, not showing null terms
    def as_dict(self):

        # GRAB STANDARD KEYS
        dict_rep = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in dict_rep.copy():
            if not dict_rep[key]:
                dict_rep.pop(key)

        # GRAB AUTHORS
        dict_rep['authors']: List[str] = []
        for author in self.authors:
            dict_rep['authors'].append(author.name)
        return dict_rep

    def __repr__(self):
        return f'<Publication({self.__dict__})>'

    @staticmethod
    def get_publications() -> List:
        """
        A METHOD TO GET ALL PUBLICATIONS IN THE TABLE
        :return: A LIST OF ALL PUBLICATIONS
        """
        session: Session = get_session()
        try:
            return session.query(Publication).all()
        finally:
            session.close()

    @staticmethod
    def create_publication(publication_data: Dict, author_data: List[Dict]):
        """
        CREATE A PUBLICATION WITH ASSOCIATED AUTHORS
        :param publication_data:  A DICT THAT CONTAINS THE KEYWORD ARGUMENTS TO BE PASSED TO THE PUBLICATION CONSTRUCTOR
        :oaram author_Data: A LIST OF DICTS THAT CONTAIN AUTHOR DATA TO BE PASSED TO THE AUTHOR CONSTRUCTOR & LINKED TO
            THE PUBLICATION
        """

        # GRAB A SESSION
        session: Session = get_session()

        # CREATE A PUBLICATION AND ADD IT TO THE SESSION
        publication: Publication = Publication(**publication_data)
        session.add(publication)

        # COMMIT IT SO THAT A PRIMARY KEY (ID) IS GENERATED
        session.commit()

        # CREATE AUTHORS WITH THE ID OF THE PUBLICATION
        for author_dict in author_data:
            # ADD THE ID OF THE PUBLICATION TO EACH AUTHOR
            author_dict['publication_id'] = publication.id
            author: Author = Author(**author_dict)
            session.add(author)

        # COMMIT THE AUTHORS
        session.commit()
        session.close()


class Author(Base):
    """
    THE CLASS CORRESPONDING TO THE AUTHORS TABLE
    """
    __tablename__ = 'authors'

    id: int = Column(Integer, primary_key=True, nullable=False)  # THE PRIMARY KEY
    publication_id: id = Column(Integer, ForeignKey("publications.id"), nullable=False)  # FOREIGN KEY TO PUBLICATIONS
    name: str = Column(String(40))
    orcid: str = Column(String(40))

    publication = relationship("Publication", back_populates="authors")

    def __repr__(self):
        return f'<Author({self.__dict__})>'

    @staticmethod
    def get_authors() -> List:
        """
        A METHOD TO GET ALL AUTHORS IN THE TABLE
        :return: A LIST OF AUTHORS
        """
        session: Session = get_session()
        try:
            return session.query(Author).all()
        finally:
            session.close()

    # presents row as dictionary, not showing null terms
    def as_dict(self):
        dict_rep = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in dict_rep.copy():
            if not dict_rep[key]:
                dict_rep.pop(key)
        return dict_rep


class Topics(Base):
    """
    CLASS CORRESPONDING TO THE TOPICS TABLE
    """

    __tablename__ = 'topics'

    id: int = Column(Integer, primary_key=True, nullable=False)  # THE PRIMARY KEY
    publication_id: id = Column(Integer, ForeignKey("publications.id"), nullable=False)  # FOREIGN KEY TO PUBLICATIONS
    predicted_topic: int = Column(Integer)
    topic1: float = Column(Float)
    topic2: float = Column(Float)
    topic3: float = Column(Float)
    topic4: float = Column(Float)
    topic5: float = Column(Float)
    topic6: float = Column(Float)
    topic7: float = Column(Float)
    topic8: float = Column(Float)
    topic9: float = Column(Float)
    topic10: float = Column(Float)

    publication = relationship("Publication", back_populates="topics")

    # DEFINE HOW TO PRINT THE TYPE
    def __repr__(self):
        return f'<Topic({self.__dict__})>'

    @staticmethod
    def get_topic_names():
        return ['topic1', 'topic2', 'topic3', 'topic4', 'topic5', 'topic6', 'topic7', 'topic8', 'topic9', 'topic10']

    @staticmethod
    def get_papers_per_topic():
        session: Session = get_session()

        count_per_topic: Dict = {
            'topic 1': session.query(func.count("*")).select_from(Topics).filter(Topics.topic1 > 0).scalar(),
            'topic 2': session.query(func.count("*")).select_from(Topics).filter(Topics.topic2 > 0).scalar(),
            'topic 3': session.query(func.count("*")).select_from(Topics).filter(Topics.topic3 > 0).scalar(),
            'topic 4': session.query(func.count("*")).select_from(Topics).filter(Topics.topic4 > 0).scalar(),
            'topic 5': session.query(func.count("*")).select_from(Topics).filter(Topics.topic5 > 0).scalar(),
            'topic 6': session.query(func.count("*")).select_from(Topics).filter(Topics.topic6 > 0).scalar(),
            'topic 7': session.query(func.count("*")).select_from(Topics).filter(Topics.topic7 > 0).scalar(),
            'topic 8': session.query(func.count("*")).select_from(Topics).filter(Topics.topic8 > 0).scalar(),
            'topic 9': session.query(func.count("*")).select_from(Topics).filter(Topics.topic9 > 0).scalar(),
            'topic 10': session.query(func.count("*")).select_from(Topics).filter(Topics.topic10 > 0).scalar()
        }

        return count_per_topic

    def as_dict(self):

        dict_rep = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in dict_rep.copy():
            if dict_rep[key] is None:
                dict_rep.pop(key)
        return dict_rep
