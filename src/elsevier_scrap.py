import urllib2
from bs4 import BeautifulSoup


def scrap_metric_data(link):
    try :
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        metrics = soup.find_all('span', attrs={'class': 'tooltip'})
        metrics = [m.text[:-1] for m in metrics]

        '''
        metrics sample output:

        Source Normalized Impact per Paper (SNIP): 5.192
        SCImago Journal Rank (SJR): 3.263
        Impact Factor: 3.371
        5-Year Impact Factor: 3.726
        '''

        snip = metrics[0].split(': ')[1]
        sjr  = metrics[1].split(': ')[1]
        imp_fact = metrics[2].split(': ')[1]
        imp_fact_5 = metrics[3].split(': ')[1]

        return snip, sjr, imp_fact, imp_fact_5
    except :
        # if no values are present or on error
        return 0.0, 0.0, 0.0, 0.0


def journal_info(link) :
    data = []
    try :
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        journals = soup.find_all('a', attrs={'class': 'journal-title'})
        for journal in journals :
            title = journal.find('span', attrs={'class':'normal-title'}).text
            link = journal['href']

            snip, sjr, imp_fact, imp_fact_5 = scrap_metric_data(link)
            info = [title, link, snip, sjr, imp_fact, imp_fact_5]

            print "[DEBUG] ", info
            data.append(info)
    except :
        pass

    return data


def fetch_all_jornals() :
    '''
    This function is used to fetch all journal links from a page.
    Elsevier returns only 20 journal links in a page.

    start : http://www.elsevier.com/journals/title/all?start_rank=1
    end : http://www.elsevier.com/journals/title/all?start_rank=3141

    :return: list of links to pages containing links to journals
    '''

    base_link = 'http://www.elsevier.com/journals/title/all?start_rank='
    start_rank = 1
    end_rank = 3141
    step = 20

    data = []
    for i in range(start_rank, end_rank + 1, step):
        link = base_link + str(i)

        print "[INFO] Fetching journals from ", link
        data.extend(journal_info(link))

    print ""
    print "[INFO] Writing all output to CSV file "

    import csv
    with open('../output/elsevier.csv', 'w') as csvfile:
        fields = ['title', 'link', 'snip', 'sjr', 'impact factor', '5 year impact factor']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for d in data :
            # normalize title
            d[0] = unicode(d[0]).encode("utf-8")

            # write output
            writer.writerow({fields[0] : d[0], fields[1] : d[1], fields[2] : d[2],
                             fields[3] : d[3], fields[4] : d[4], fields[5] : d[5]})

    print "[INFO] Done writing CSV file"

fetch_all_jornals()



