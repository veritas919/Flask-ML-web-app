from flask import request, jsonify
from queries import mashup
import queries
from typing import Dict, List, Optional, Set

# LAB 1 QUERY 1
def coauthors():
    author: str = request.args.get('author', None)
    query: str = f'get coauthors for author with name "{author}"'

    if author is None:
        return jsonify({})
    coauthors: List[str] = list(queries.mysql.get_coauthors(author))
    return jsonify(coauthors)


# PAPER METADATA
def paper_metadata():
    paper_title: Optional[str] = request.args.get('title', None)

    # MAKE SURE WE HAVE A TITLE
    if paper_title is None:
       jsonify({})

    metadata: Dict = queries.mysql.get_paper_metadata(paper_title)
    return jsonify(metadata)


# JOURNAL METADATA
def journal_metadata():
    journal_search: Optional[str] = request.args.get("journal", None)
    volume_search: Optional[str] = request.args.get("volume", None)

    if journal_search is None or volume_search is None:
        jsonify({})

    book_papers_metadata: List[Dict] = queries.mysql.get_article_info_for_book(journal_search, int(volume_search))
    return jsonify(book_papers_metadata)

# CONFERENCE PAPER METADATA
def conference_paper_metadata():
    conference_search: Optional[str] = request.args.get("conference", None)
    year_search: Optional[str] = request.args.get("year", None)

    if year_search is None or conference_search is None:
        return jsonify({})

    book_papers_metadata: List[Dict] = queries.mysql.get_inproceeding_info_for_book(conference_search, int(year_search))
    return jsonify(book_papers_metadata)


# BONUS QUERY 1
def bonus_query_2_1():
    titles_in_SOSE = queries.xquery.bonus2_1()
    return jsonify(titles_in_SOSE)


# BONUS QUERY 2
def bonus_query_2_2():
    researcher_search: str = request.args.get("researcher", "Jia Zhang")
    year_search: int = int(request.args.get("year", "2014"))

    query = f'Get the titles of all articles published by {researcher_search} in {year_search}'

    titles = queries.xquery.bonus2_2(researcher_search, year_search)
    return jsonify(titles)


# BONUS QUERY 3
def bonus_query_2_3():
    authors = queries.xquery.bonus2_3()
    query: str = f'Display all authors who have published more than 10 papers in the area of SOSE'
    return jsonify(authors)


# BONUS QUERY 4
def bonus_query_2_4():
    paper_search: Optional[str] = request.args.get('paper', None)
    query: str = f'get a paper named {paper_search} and list its publication metadata'
    if paper_search is None:
       return jsonify({})

    data = queries.xquery.bonus2_4(paper_search)
    return jsonify(data)


# RETURN THE RAW JSON
def lab2_mashup_1():
    researcher_search: str = request.args.get("researcher")
    year_search = request.args.get("year")

    medatadata: Dict = {}
    if researcher_search is None or year_search is None:
        metadata = {}

    metadata = mashup.mash_up_1(researcher_search, year_search)
    return jsonify(metadata)

def lab2_mashup_2():
    coauthors = mashup.mash_up_2()
    return jsonify(coauthors)