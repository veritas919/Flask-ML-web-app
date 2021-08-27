from xml.dom import minidom
import xmlparser
from typing import List, Dict


# convert dblp_abstract_dataset.xml to a csv with title, abstract 
def abstracts_and_title_to_csv():

    dom = minidom.parse('dblp_abstract_dataset.xml')
    articles: List = dom.getElementsByTagName("article")
    article_abstracts: List = []

    inproceedings: List = dom.getElementsByTagName("inproceedings")
    inproceedings_abstracts: List = []

    file = open('abstract_title.csv','a', encoding = 'utf-8')
    file.write('title' + "DELIMITER" + "abstract" + "\n")


    # Process ABSTRACTS
    for article in articles:
        title = xmlparser.get_child_tag_data(article, 'title')
        title = title.strip().rstrip()
        abstract = xmlparser.get_child_tag_data(article, 'abstract')
        abstract = abstract.strip().rstrip()
        file.write(title + 'DELIMITER' + abstract + "\n")


    for inproceeding in inproceedings:
        title = xmlparser.get_child_tag_data(inproceeding, 'title')
        title = title.strip() 
        abstract = xmlparser.get_child_tag_data(inproceeding, 'abstract')
        abstract = abstract.strip().rstrip()
        file.write(title + 'DELIMITER' + abstract + "\n")

    file.close() 

if __name__ == "__main__":
    abstracts_and_title_to_csv()
