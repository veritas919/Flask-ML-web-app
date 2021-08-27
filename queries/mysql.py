from database import Author, Publication, get_session
from typing import List, Dict, Set
from sqlalchemy import select
from sqlalchemy.orm import Session


#####################################################################
# QUERY 1
# GIVEN AN AUTHOR NAME, LIST ALL THEIR CO-AUTHORS
######################################################################
def get_coauthors(author_name: str) -> Set[str]:
    print(f'Getting coauthors for {author_name}')
    author_name = author_name.strip()

    # GET ALL INSTANCES OF THE AUTHOR, AND ALL PUBLICATIONS THEY'VE MADE
    session: Session = get_session()
    #print("Getting all isntances of the author")
    #authors: List[Author] = session.query(Author).filter_by(name=author_name).all()
    #print("getting all of their publications")
    #publications: List[Publication] = [author.publication for author in authors]

    # FOR EACH OF THOSE PUBLICATIONS, FIND ALL OF THE AUTHORS
    print("finding coauthors")
    coauthors: Set[str] = set()
    for author in session.query(Author).filter_by(name=author_name).all():
        print(f'\tcoauthors in {author.publication.title}')
        for author in author.publication.authors:
            coauthors.add(author.name)
            print(f'\t\t{author.name}')


    coauthors.remove(author_name)
    session.close()
    return coauthors


#####################################################################
# QUERY 2
# GIVEN A PAPER NAME, LIST ITS PUBLICATION METADATA
######################################################################
def get_paper_metadata(paper_title: str) -> Dict:
    session: Session = get_session()
    paper: Publication = session.query(Publication)\
        .filter(Publication.title == paper_title)\
        .filter(Publication.type == 'article')\
        .first()

    session.close()
    return paper.as_dict()


#####################################################################
# QUERY 3
# GIVEN A JOURNAL NAME, YEAR, AND ISSUE, FIND OUT THE METADATA OF ALL
# THE PAPERS PUBLISHED IN THE BOOK
######################################################################
def get_article_info_for_book(journal_title: str, volume: int) -> List[Dict]:
    session: Session = get_session()
    count: int = 0
    results: List[Dict] = []
    for article in session.query(Publication)\
            .filter(Publication.journal == journal_title)\
            .filter(Publication.volume == volume)\
            .filter(Publication.type == 'article'):
        # print(count)
        article_dict_format = article.as_dict()
        results.append(article_dict_format)
        # count = count+1
    session.close()
    return results


#####################################################################
# QUERY 4
# GIVEN A CONFERENCE NAME AND A YEAR, FIND OUT THE METADATA OF ALL THE
# PAPERS PUBLISHED IN THE BOOK (THE PROCEEDINGS)
######################################################################
def get_inproceeding_info_for_book(conference: str, year: int) -> List[Dict]:
    session: Session = get_session()
    count: int = 0
    results: List[Dict] = []
    for inproceeding in session.query(Publication)\
            .filter(Publication.booktitle == conference)\
            .filter(Publication.year == year)\
            .filter(Publication.type == 'inproceedings'):
        # print(count)
        inproceeding_dict_format = inproceeding.as_dict()
        results.append(inproceeding_dict_format)
        # count = count+1
    session.close()
    return results

#####################################################################
# LAB 2 QUERY 2
# FIND ALL OF THE COAUTHORS FOR A LIST OF AUTHORS
######################################################################
def get_coauthor_names(author_names: List[str]) -> List[str]:
    session: Session = get_session()
    publication_ids: Set[int] = set()

    # GET IDs of all the publications that the authors in the list have worked on
    for author in session.query(Author).filter(Author.name.in_(author_names)):
        publication_ids.add(author.publication_id)
    print(publication_ids)

    # FIND THE NAMES OF ALL AUTHORS THAT WORKED ON THOSE PUBLICATION NAMES
    collaborators: Set[str] = set()
    for a in session.query(Author).filter(Author.publication_id.in_(list(publication_ids))):
        collaborators.add(a.name)

    # REMOVE THE ORIGINAL AUTHORS FROM THE COAUTHORS
    coauthors: Set[str] = collaborators - set(author_names)
    return list(coauthors)

def get_coauthors_for_productive_authors(author_names: List[str]) -> Dict:
    session: Session = get_session()

    # NON-DISTINCT AUTHORS
    productive_authors: List[Author] = session.query(Author).filter(Author.name.in_(author_names))
    print(author_names)
    publication_ids: Set[int] = set()

    # BUILD LIST OF PUBLICATION IDS
    for author in productive_authors:
        publication_ids.add(author.publication_id)
    print()
    print(publication_ids)
    # GET LIST OF ALL COLLABORATORS
    collaborators: List[Author] = session.query(Author).filter(Author.publication_id.in_(list(publication_ids)))

    # MAP COLLABORATORS TO PUBLICATION IDS
    pub_to_collaborators: Dict = {}
    for id in publication_ids:
        pub_to_collaborators[id] = set()
    for collaborator in collaborators:
        pub_to_collaborators[collaborator.publication_id].add(collaborator.name)
    print()
    print(f'pub to collaborators: {pub_to_collaborators}')

    # CORRELATE EACH AUTHOR TO THEIR PUBLICATIONS
    author_to_pub_ids: Dict = {}
    for author in productive_authors:
        author_to_pub_ids[author.name] = set()
    for author in productive_authors:
        author_to_pub_ids[author.name].add(author.publication_id)
    print()
    print(f'author to pub ids: {author_to_pub_ids}')


    # CORRELATED EACH AUTHOR TO THEIR PUBLICATIONS BY ADDING THE SETS TOGETHER, AND THEN SUBTRACTING THEIR OWN NAME FROM IT
    author_to_collaborators: Dict = {}
    for author in productive_authors:
        author_to_collaborators[author.name] = set()
    # FOR EACH AUTHOR
    for author in author_to_pub_ids:

        # FOR EACH OF THEIR PUBLICATIONS
        for pub_id in author_to_pub_ids[author]:

            # UNION IT TOGETHER
            author_to_collaborators[author] = author_to_collaborators[author].union(pub_to_collaborators[pub_id])

    # REMOVE EACH AUTHOR FROM THEIR LIST OF COLLABORATORS
    for author in author_to_collaborators:
        author_to_collaborators[author].discard(author)
    print()
    print(f'author to collaborators: {author_to_collaborators}')

    # REMOVE EACH AUTHOR FROM THEIR OWN SET
    for author in productive_authors:
        author_to_collaborators[author.name].discard(author.name)

    for author in productive_authors:
        author_to_collaborators[author.name] = list(author_to_collaborators[author.name])

    return author_to_collaborators