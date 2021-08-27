import xml.etree.ElementTree as ET
from typing import List, Dict, Set


# Part 2....bonus

print("Let the bonus points querying begin")
print()

#############################################################################
# BONUS 2.1
#############################################################################

def bonus2_1() -> List[str]:
    tree = ET.parse('./data/papers_clean.xml')
    root = tree.getroot()

    print()
    print("BONUS 2.1")
    print()

    SOSEtitles = []
    for elm in root.findall("./article"):   # if we only want them from articles. If from articles OR improceedings, change to ("./")
        for titleEl in elm.findall("title"):
            titleText = titleEl.text.strip()
            print(titleText)
            SOSEtitles.append(titleText)
    return SOSEtitles


#############################################################################
# BONUS 2.2
#############################################################################

def bonus2_2(researcher_search: str, year_search: int) -> List[str]:
    tree = ET.parse('./data/papers_clean.xml')
    root = tree.getroot()

    print()
    print("Bonus 2.2")

    researcher_search = researcher_search.strip()
    year_str: str = str(year_search)


    titles = []
    for elm in root.findall("./article"):   # if we want them from only articles. If from articles or improceedings, change to ("./")
        yearText = elm.find("year").text.strip()

        for subtagElm in elm.findall("./author"):
            authorText = subtagElm.text.strip() # remove leading and trailing whitespace on subtag text
            if authorText == researcher_search and yearText == year_str:
                titles.append(elm.find("title").text)
                #print (elm.find("title").text)  # print titles of relevant articles
    return titles

###################################################################
# Bonus 2.3
###################################################################

def bonus2_3():
    tree = ET.parse('./data/papers_clean.xml')
    root = tree.getroot()

    print()
    print("Bonus 2.3")

    # create dictionary of author : number of papers on SOSE
    author_to_SOSE_paper_count = {}
    titles = []
    for elm in root.findall("./"):   # from articles or improceedings
        for subtagElm in elm.findall("./author"):
            authorText = subtagElm.text.strip() # remove leading and trailing whitespace on subtag text
            author_to_SOSE_paper_count [authorText] = 0

    for elm in root.findall("./"):  # from articles OR improceedings
        for titleEl in elm.findall("title"):
            for authorEl in elm.findall("author"):
                titleText = titleEl.text.strip()
                authorText = authorEl.text.strip()
                author_to_SOSE_paper_count[authorText] = author_to_SOSE_paper_count[authorText] + 1

    # create set of authors who have published > 10 papers related to SOSE
    author_set = set()

    for key in author_to_SOSE_paper_count:
        #print(key, author_to_SOSE_paper_count[key])
        if author_to_SOSE_paper_count[key] > 10:
            author_set.add(key)
    return author_set

#########################################################################
# Bonus 2.4
########################################################################

def bonus2_4(paper_search):
    tree = ET.parse('./data/papers_clean.xml')
    root = tree.getroot()

    print("\n")
    print("Bonus 2.4")

    paper_search = paper_search.strip()  # remove leading and trailing whitespace

    result = {}
    for elm in root.findall("./"):
        for titleEl in elm.findall("title"):
            titleText = titleEl.text.strip()
            if titleText == paper_search:
                print("Paper type: ", elm.tag)
                result["type"] = elm.tag
                print("Date: ", elm.attrib['mdate'])
                result["mdate"] = elm.attrib['mdate']
                for subInfo in elm.findall("./"):
                    result[subInfo.tag] = subInfo.text
                    print(subInfo.tag, ": ", subInfo.text)

    return result