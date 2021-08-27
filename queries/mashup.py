from queries import mysql, xquery #.get_paper_metadata, get_coauthors
#from queries import bonus2_2, bonus2_3
from typing import Dict

def mash_up_1(name, year):
    articles_metadata = []
    titles = xquery.bonus2_2(name, year)
    for title in titles:
        articles_metadata.append(mysql.get_paper_metadata(title))

    return articles_metadata

def mash_up_2() -> Dict:
    productive_authors = xquery.bonus2_3()
    print(len(productive_authors))

    return mysql.get_coauthors_for_productive_authors(productive_authors)
