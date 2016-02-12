
import pymongo

client = pymongo.MongoClient("localhost", 27017)

# db name - scibase
db = client.scibase

# collection
db.aminer


print "[INFO] Processing papers"

file = open("../data/aminer_publications.txt")
papers = {}
j = 0;
line = file.readline()

while line :
    paper = {}
    paper['references'] = []
    while line !=  '  \r\n' :
        line = line.strip()

        '''
        #index ---- index id of this paper
        #* ---- paper title
        #@ ---- authors (separated by semicolons)
        #o ---- affiliations (separated by semicolons, and each affiliaiton corresponds to an author in order)
        #t ---- year
        #c ---- publication venue
        #% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
        #! ---- abstract
        '''

        if line.startswith('#index') : paper['index']        = line[len('#index'):]
        if line.startswith('#*') :     paper['title']        = line[len('#*'):]
        if line.startswith('#@') :     paper['authors']      = line[len('#@'):].split(',')
        if line.startswith('#o') :     paper['affiliations'] = line[len('#o'):].split(',')
        if line.startswith('#t') :     paper['year']         = line[len('#t'):]
        if line.startswith('#c') :     paper['publication']  = line[len('#c'):]
        if line.startswith('#!') :     paper['abstract']     = line[len('#!'):]
        if line.startswith('#%') :     
                ref = line[len('#%'):]
                if len(ref) != 0 :     paper['references'].append(ref)

        line = file.readline()


    db.aminer.insert_one(paper)

    print "[INFO] inserted into db paper", paper['index']

    line = file.readline()

file.close()

