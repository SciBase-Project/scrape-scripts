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

    try:
        searchObj = re.search(r'(.*)arnumber=(\d*).*', link)
        if searchObj:
            return searchObj.group(2)
        else:
            return None
    except:
        return None


def get_details(id):
    link = DETAILS_LINK + str(id)

    details = {}

    abstract = ""

    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        # abstract
        divs = soup.find_all("div", attrs={"class": "article"})
        for div in divs:
            if div.find("p") != None:
                abstract = div.find("p").string
                break

        details["abstract"] = abstract

        conference = soup.find("meta", attrs={"name": "citation_conference"})
        publisher = soup.find("meta", attrs={"name": "citation_publisher"})
        title = soup.find("meta", attrs={"name": "citation_title"})
        date = soup.find("meta", attrs={"name": "citation_date"})
        volume = soup.find("meta", attrs={"name": "citation_volume"})
        issue = soup.find("meta", attrs={"name": "citation_issue"})
        firstpage = soup.find("meta", attrs={"name": "citation_firstpage"})
        lastpage = soup.find("meta", attrs={"name": "citation_lastpage"})
        doi = soup.find("meta", attrs={"name": "citation_doi"})
        isbn = soup.find("meta", attrs={"name": "citation_isbn"})
        journal_title = soup.find("meta", attrs={"name": "citation_journal_title"})


        pages = soup.find("dt", text="Page(s):")
        meeting_date = soup.find("dt", text="Meeting Date :")
        inspec = soup.find("dt", text="INSPEC Accession Number:")
        conference_location = soup.find("dt", text="Conference Location :")
        issn = soup.find("dt", text="ISSN :")
        date_publication = soup.find("dt", text="Date of Publication :")
        date_current_version = soup.find("dt", text="Date of Current Version :")
        issue_date = soup.find("dt", text="Issue Date :")
        sponsor = soup.find("dt", text="Sponsored by :")


        if conference : details["conference"] = conference["content"]
        if publisher : details["publisher"] = publisher["content"]
        if title : details["title"] = title["content"]
        if date : details["date"] = date["content"]
        if volume : details["volume"] = volume["content"]
        if issue : details["issue"] = issue["content"]
        if firstpage : details["firstpage"] = firstpage["content"]
        if lastpage : details["lastpage"] = lastpage["content"]
        if doi : details["doi"] = doi["content"]
        if isbn : details["isbn"] = isbn["content"]
        if journal_title : details["journal_title"] = journal_title["content"]

        try :
            if pages : details["pages"] = " ".join(pages.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if meeting_date : details["meeting_date"] = " ".join(meeting_date.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if inspec : details["inspec"] = " ".join(inspec.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if conference_location : details["conference_location"] = " ".join(conference_location.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if issn : details["issn"] = " ".join(issn.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if date_publication : details["date_publication"] = " ".join(date_publication.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if date_current_version : details["date_current_version"] = " ".join(date_current_version.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if issue_date : details["issue_date"] = " ".join(issue_date.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if sponsor : details["sponsor"] = sponsor.findNext("dd").find("a").text
        except : pass


    except Exception,e: print str(e)


    return details


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

    return authors


def get_references(id):
    link = REFERENCE_LINK + str(id)

    references = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        divs = soup.find_all("div", attrs={"class": "links"})

        for div in divs:
            a_tags = div.find_all("a")

            arnumber = get_id_from_link(a_tags[0]["href"])

            if arnumber != None:
                references.append(arnumber)

    except:
        pass

    return references


def get_citations(id):
    link = CITATIONS_LINK + str(id)

    citations = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        divs = soup.find_all("div", attrs={"class": "links"})

        for div in divs:
            a_tags = div.find_all("a")

            arnumber = get_id_from_link(a_tags[0]["href"])

            if arnumber != None:
                citations.append(arnumber)

    except:
        pass

    return citations


def get_keywords(id):
    link = KEYWORDS_LINK + str(id)

    keywords = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        meta = soup.find("meta", attrs={"name": "citation_keywords"})

        for keyword in meta["content"].strip().split(";"):
            keywords.append(keyword.strip())

    except:
        pass

    return keywords


def get_article(arnumber):
    article = {}
    article["arnumber"] = arnumber
    article["details"] = get_details(arnumber)
    article["authors"] = get_authors(arnumber)
    article["references"] = get_references(arnumber)
    article["citations"] = get_citations(arnumber)
    article["keywords"] = get_keywords(arnumber)

    return article


def store_article(arnumber) :
    import pymongo
    client = pymongo.MongoClient("localhost", 27017)
    db = client.scibase
    db.ieee.insert_one(get_article(arnumber))



if __name__ == "__main__":
    import pymongo
    client = pymongo.MongoClient("localhost", 27017)
    db = client.scibase

    for arn in xrange(1, 10**1) :
        print "\nFetching article", arn

        article = get_article(arn)
        print article

        db.ieee.insert_one(article)

        print "Done storing article", arn



