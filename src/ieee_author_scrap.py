AUTHORS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='


import urllib2
from bs4 import BeautifulSoup

data = []

def ieee_authors(link):

    print link
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        metas = soup.find_all("meta", attrs={"name": "citation_author"})

        name = ""

        for meta in metas:
            if meta['name'] == 'citation_author':
                name = meta['content']
                break

        span = soup.find("span", id='authorAffiliations')
        out = span.get('class')

        aff = "".join(out)

        data.append({"author_name" : name, "author_affiliations" : aff})

    except:
        print "error"
        pass


for i in range(200, 700):
    link = AUTHORS_LINK + str(i)
    ieee_authors(link)


import json
file = open("../output/ieee_author_affliation.json", "w")
file.write(json.dumps(data, indent=4))
file.close()