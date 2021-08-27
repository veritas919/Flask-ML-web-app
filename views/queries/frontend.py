from flask import render_template, jsonify, request
import queries
from utilities.formatter import format_dict
from typing import List, Dict, Set, Optional
import pprint
from queries import mashup, xquery, mysql

###################################################################
# VIEWS FOR THE REQUIRED QUERIES
###################################################################

# PAPER METADATA
def coauthors():
    author: str = request.args.get('author', None)
    query: str = f'get coauthors for author with name "{author}"'

    if author is None:
        return render_template('query_results.html.jinja2', query=query, data=[])
    coauthors: List[str] = list(queries.mysql.get_coauthors(author))
    coauthors_str: str = format_dict(coauthors)
    return render_template('query_results.html.jinja2', query=query, data=coauthors_str)


# PAPER METADATA
def paper_metadata():
    paper_title: Optional[str] = request.args.get('title', None)
    query: str = f'get metadata for a paper with the title "{paper_title}"'

    # MAKE SURE WE HAVE A TITLE
    if paper_title is None:
        return render_template('query_results.html.jinja2', query=query, data={})

    metadata: Dict = queries.mysql.get_paper_metadata(paper_title)
    metadata_str: str = format_dict(metadata)
    return render_template('query_results.html.jinja2', query=query, data=metadata_str)


# JOURNAL METADATA
def journal_metadata():
    journal_search: Optional[str] = request.args.get("journal", None)
    volume_search: Optional[str] = request.args.get("volume", None)

    query: str = f'get metadata for articles published in volume {volume_search} of {journal_search}'

    if journal_search is None or volume_search is None:
        return render_template('query_results.html.jinja2', query=query, data=[])

    book_papers_metadata: List[Dict] = queries.mysql.get_article_info_for_book(journal_search, int(volume_search))
    book_papers_metadata_str: str = format_dict(book_papers_metadata)
    return render_template('query_results.html.jinja2', query=query, data=book_papers_metadata_str)

# CONFERENCE PAPER METADATA
def conference_paper_metadata():
    conference_search: Optional[str] = request.args.get("conference", None)
    year_search: Optional[str] = request.args.get("year", None)

    query: str =f'get metadata for papers from conference {conference_search} in {year_search}'
    if year_search is None or conference_search is None:
        print("None!")
        return render_template('query_results.html.jinja2', query=query, data=[])

    book_papers_metadata: List[Dict] = queries.mysql.get_inproceeding_info_for_book(conference_search, int(year_search))
    book_papers_metadata_str: str = format_dict(book_papers_metadata)
    return render_template('query_results.html.jinja2', query=query, data=book_papers_metadata_str)

###################################################################
# VIEWS FOR THE XQUERY QUERIES
###################################################################

# BONUS QUERY 1
def bonus_query_2_1():
    titles_in_SOSE = queries.xquery.bonus2_1()

    query: str = "Get all titles published in SOSE"
    titles_list: str = format_dict(titles_in_SOSE)
    return render_template('query_results.html.jinja2', query=query, data=titles_list)

# BONUS QUERY 2
def bonus_query_2_2():
    researcher_search: str = request.args.get("researcher", "Jia Zhang")
    year_search: int = int(request.args.get("year", "2014"))

    query = f'Get the titles of all articles published by {researcher_search} in {year_search}'

    titles = queries.xquery.bonus2_2(researcher_search, year_search)
    titles_str: str = format_dict(titles)
    return render_template('query_results.html.jinja2', query=query, data=titles_str)

# BONUS QUERY 3
def bonus_query_2_3():
    authors = queries.xquery.bonus2_3()
    query: str = f'Display all authors who have published more than 10 papers in the area of SOSE'
    authors_str: str = format_dict(authors)
    return render_template('query_results.html.jinja2', query=query, data=authors_str)

# BONUS QUERY 4
def bonus_query_2_4():

    paper_search: Optional[str] = request.args.get('paper', None)
    query: str = f'get a paper named {paper_search} and list its publication metadata'
    if paper_search is None:
        return render_template('query_results.html.jinja2', query=query, data = {})
    
    data = queries.xquery.bonus2_4(paper_search)
    data_str: str = format_dict(data)
    return render_template('query_results.html.jinja2', query=query, data=data_str)

###################################################################
# VIEWS FOR THE LAB 2 QUERIES
###################################################################
def lab2_mashup1():
    researcher_search: str = request.args.get("researcher")
    year_search = request.args.get("year")
    query: str = "Given a researcher's name and a year, list all published articles metadata"
    if researcher_search is None or year_search is None:
        return render_template('query_results.html.jinja2', query=query, data={})

    metadata = mashup.mash_up_1(researcher_search, year_search)
    data_str: str = format_dict(metadata)
    return render_template("query_results.html.jinja2", query=query, data=data_str)

def lab2_mashup2():
    coauthors = mashup.mash_up_2()
    data_str = format_dict(coauthors)
    query: str = "For the productive authors in SOSE, list all of their coauthors"
    return render_template("query_results.html.jinja2", query=query, data=data_str)