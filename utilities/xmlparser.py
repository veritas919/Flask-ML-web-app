from xml.dom import minidom
from typing import List, Tuple, Any, Dict, Optional


def get_child_tag(parent, tag_name: str) -> Any:
    """
    GET A TAG WITH A GIVEN NAME GIVEN A PARENT
    :param parent: THE PARENT TAG
    :param tag_name: THE NAME OF THE CHILD TAG
    :return: THE CHILD TAG
    """
    try:
        return parent.getElementsByTagName(tag_name)[0]
    except IndexError as e:
        return None


def get_child_tags(parent, tag_name: str) -> List[Any]:
    """
    GET ALL TAGS WITH A GIVEN NAME FROM A PARENT
    :param parent: THE PARENT TAG
    :param tag_name: THE NAME OF THE CHILD TAGS
    :return: A LIST OF CHILD TAGS
    """
    return parent.getElementsByTagName(tag_name)


def get_tag_attr(tag, attr_name) -> Optional[str]:
    """
    GET THE VALUE OF AN ATTRIBUTE OF A TAG
    :param tag: THE TAG TO FETCH THE ATTRIBUTE FROM
    :param attr_name: THE NAME OF THE ATTRIBUTE
    :return: THE VALUE OF THE ATTRIBUTE
    """
    if tag is None:
        return None
    return tag.getAttribute(attr_name)


def get_tag_data(tag) -> Optional[str]:
    """
    GET THE DATA CONTENTS OF AN XML TAG
    :param tag: THE TAG TO GET DATA FROM
    :return: THE CONTENTS OF THE TAG
    """
    if tag is None: return None
    return tag.firstChild.nodeValue


def get_child_tag_data(parent, tag_name: str) -> str:
    """
    RETURN THE DATA FOR A CHILD TAG ELEMENT
    :param parent: THE PARENT TAG
    :param tag_name: THE NAME OF THE CHILD TAG
    :return: THE DATA OF THE CHILD TAG
    """
    return get_tag_data(get_child_tag(parent, tag_name))


def get_childrens_tag_data(parent, tag_name: str) -> List[str]:
    """
    RETURN A LIST DATA FOR ALL CHILD ELEMENTS OF A GIVEN TYPE
    :param parent: THE PARENT TAG
    :param tag_name: THE NAME OF THE CHILD TAGS TO GET
    :return: A LIST OF TAG DATA (STRINGS)
    """
    return [get_tag_data(tag) for tag in get_child_tags(parent, tag_name)]


def get_tag_name(tag) -> str:
    """
    GET THE NAME OF A TAG
    :param tag: THE TAG
    :return: THE NAME
    """
    return tag.firstChild.tagName


def process_publication(publication_tag) -> Dict:
    """
    RETURN A DICTIONARY REPRESENTING EITHER A CONFERENCE PAPER OR AN ARTICLE THAT CAN THEN BE EXPLODED INTO A 
    PUBLICATION OBJECT. 
    :param publication_tag: THE PUBLICATION TO GENERATE A DICT FOR
    :return: THE DICTIONARY TO EXPLODE
    """

    return {
        'type': publication_tag.tagName,
        'title': get_child_tag_data(publication_tag, 'title'),
        'booktitle': get_child_tag_data(publication_tag, 'booktitle'),
        'pages': get_child_tag_data(publication_tag, 'pages'),
        'year': int(get_child_tag_data(publication_tag, 'year')) if get_child_tag_data(publication_tag,
                                                                                       'year') else None,
        'address': get_child_tag_data(publication_tag, 'address'),
        'journal': get_child_tag_data(publication_tag, 'journal'),
        'volume': int(get_child_tag_data(publication_tag, 'volume')) if get_child_tag_data(publication_tag,
                                                                                           'volume') else None,
        'number': int(get_child_tag_data(publication_tag, 'number')) if get_child_tag_data(publication_tag,
                                                                                           'number') else None,
        'month': get_child_tag_data(publication_tag, 'month'),
        'url': get_child_tag_data(publication_tag, 'url'),
        'ee': get_child_tag_data(publication_tag, 'ee'),
        'cdrom': get_child_tag_data(publication_tag, 'cdrom'),
        'cite': get_child_tag_data(publication_tag, 'cite'),
        'publisher': get_child_tag_data(publication_tag, 'publisher'),
        'note': get_child_tag_data(publication_tag, 'note'),
        'crossref': get_child_tag_data(publication_tag, 'crossref'),
        'isbn': get_child_tag_data(publication_tag, 'isbn'),
        'series': get_child_tag_data(publication_tag, 'series'),
        'school': get_child_tag_data(publication_tag, 'school'),
        'chapter': int(get_child_tag_data(publication_tag, 'chapter')) if get_child_tag_data(publication_tag,
                                                                                             'chapter') else None,
        'publnr': get_child_tag_data(publication_tag, 'publnr'),

        'series_href': get_tag_attr(get_child_tag(publication_tag, 'series'), 'href') if get_child_tag(publication_tag,
                                                                                                       'series') else None,
        'mdate': get_tag_attr(publication_tag, 'mdate'),
        'key': get_tag_attr(publication_tag, 'key'),
        'ee_type': get_tag_attr(get_child_tag(publication_tag, 'ee'), type)

    }


def process_authors(publication_tag) -> List[Dict]:
    """
    GET A LIST OF AUTHORS FOR A PUBLICATION
    :param publication_tag: THE PUBLICATION TAG TO GET AUTHORS FOR
    :return: A LIST OF AUTHOR STRINGS
    """
    author_data: List[Dict] = []
    for author_tag in get_child_tags(publication_tag, "author"):
        author_data.append({
            'name': get_tag_data(author_tag),
            'orcid': get_tag_attr(author_tag, 'orcid') or None
        })

    return author_data


def minidom_parse(filepath: str) -> Tuple[List[Dict], List[List[Dict]]]:
    """
    PARSE THE XML FILE INTO THE DATABASE

    :param filepath: PATH TO THE XML FILE
    :return:
    """

    # RETURN LISTS
    publications: List[Dict] = []
    paper_authors: List[List[Dict]] = []

    # SEARCH DOM FOR TAGS WERE' LOOKING FOR
    dom = minidom.parse(filepath)

    # GRAB ALL INPROCEEDINGS AND ARTICLES
    conference_papers: List = dom.getElementsByTagName("inproceedings")
    articles: List = dom.getElementsByTagName("article")

    # GRAB CONFERENCE PAPERS/PROCEEDINGS
    for paper in conference_papers:
        # PROCESS PUBLICATION AND AUTHORS
        paper_data: Dict = process_publication(paper)
        author_data: List[Dict] = process_authors(paper)

        publications.append(paper_data)
        paper_authors.append(author_data)

    # HANDLE ARTICLES AND ADD THEM TO PUBLICATIONS TOO
    for article in articles:
        # PROCESS PUBLICATION AND AUTHORS
        article_data: Dict = process_publication(article)
        author_data: List[Dict] = process_authors(article)

        publications.append(article_data)
        paper_authors.append(author_data)


    return (publications, paper_authors)
