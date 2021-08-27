# we ran this file once, 'python clean_data.py' in the terminal in the data folder to clean up the dblp-soc-papers.xml file
# so that we could use XQuery to parse the XML document for Part 2

'''
import re
import codecs

print("~~~About to clean XML file~~~")

# Clean .xml file, so ElementTree can be used on xml file

f1 = codecs.open('dblp-soc-papers.xml', encoding="utf-8")
text = f1.read()
text_clean = re.sub (r'&+([a-zA-Z]*);+', 'e', text)

with open('papers_clean.xml', 'w') as file:
  file.write(text_clean)

'''