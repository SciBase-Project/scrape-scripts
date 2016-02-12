DETAILS_LINK = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber='
AUTHORS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='
REFERENCE_LINK = 'http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber='
CITATIONS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?arnumber='
KEYWORDS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber='
METRICS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractMetrics.jsp?arnumber='


import urllib2
from bs4 import BeautifulSoup

def get_id_from_link(link):
    import re
    try :
        searchObj = re.search(r'(.*)arnumber=(\d*).*', link)
        if searchObj:
            return searchObj.group(2)
        else:
            return None
    except :
        return None



def get_details(id):
    link = DETAILS_LINK + str(id)

    abstract = ""
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        # abstract
        divs = soup.find_all("div", attrs={"class": "article"})
        for div in divs :
            if div.find("p") != None :
                abstract =  div.find("p").string
                break

        print abstract

    except:
        pass

    print "[DEBUG] Authors", abstract
    return



def get_authors(id):
    link = AUTHORS_LINK + str(id)

    authors = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        metas = soup.find_all("meta", attrs={"name": "citation_author"})

        for meta in metas:
            if meta['name'] == 'citation_author':
                authors.append(meta['content'])
    except:
        pass

    print "[DEBUG] Authors", authors
    return



def get_references(id):
    link = REFERENCE_LINK + str(id)

    references = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        divs = soup.find_all("div", attrs={"class": "links"})

        for div in divs:
            a_tags = div.find_all("a")

            arnumber =  get_id_from_link(a_tags[0]["href"])

            if arnumber != None :
                references.append(arnumber)

    except:
        pass

    print "[DEBUG] References", references
    return



def get_citations(id):
    link = CITATIONS_LINK + str(id)

    citations = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        divs = soup.find_all("div", attrs={"class": "links"})

        for div in divs:
            a_tags = div.find_all("a")

            arnumber =  get_id_from_link(a_tags[0]["href"])

            if arnumber != None :
                citations.append(arnumber)

    except:
        pass

    print "[DEBUG] Citations", citations
    return


def get_keywords(id):
    link = KEYWORDS_LINK + str(id)

    keywords = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        meta = soup.find("meta", attrs={"name": "citation_keywords"})

        for keyword in meta["content"].strip().split(";") :
            keywords.append(keyword.strip())

    except:
        pass

    print "[DEBUG] Keywords", keywords
    return

arnum = "965977"
#get_authors(arnum)
#get_references(arnum)
#get_citations(arnum)
#get_keywords(arnum)
get_details(arnum)
