#!/usr/bin/python

import csv
from array import array

# I think I will do this for Season 4, which we have gold standard data for.
# Remove blanks? Yes. They won't add anything right now, I don't think.
# Remove expert answers? Probably should...
#   but I'll start first with the expert answers. I should be able to get a
#   really good result. Then I'll remove them.

# Read in a file of solutions in the format:
# pull out: ZoonID,User,Species, with user and species as integers

# Go through and pick a species. Transform file so that there is one
# line for each Capture-User and the Answer is 1 if they said that species
# is there and -1 if not.

filename = "season4.csv"

species = 47 # wildebeest

xij = dict()
yji = dict()

total = 0

# open file
with open(filename,'rb') as fh:
    freader = csv.reader(fh,delimiter=',')

    # get rid of header
    freader.next()

    # and go through line by line
    for item in freader:

        subj = item[0]
        user = int(item[1])
        spp = int(item[2])
    
        # create a dictionary for each capture in xij
        if not xij.has_key(subj):
            xij[subj] = dict()

        # create an array for each capture-user
        if not xij[subj].has_key(user):
            xij[subj][user] = array('i',[-1,0,0,0,0,0,0,0])
        
        # create a dictionary for each user in yji
        if not yji.has_key(user):
            yji[user] = dict()

        # create and array for each user-capture
        if not yji[user].has_key(subj):
            yji[user][subj] = array('i',[-1,1,0,0,0,0,0,0])

        # and note that it's 1 if that animal was seen
        if spp==species:
            xij[subj][user][0] = 1
            yji[user][subj][0] = 1

        # just keep track of how many there are to do
        total = total + 1

print "total of " + str(total) + " lines read\n"

# now we do the algorithm.
# 1. we already initialized all users to have reliability 1

counter = 0
thous = 0

# 2A. update each xij
for subj in xij:
    
    for user in xij[subj]:

        counter = counter + 1
        if counter == 100000:
            thous = thous + 1
            counter = 0
            print str(thous) + "00,000 xij edges processed"

        # get all users other than the target user
        allbutme = xij[subj].keys()
        allbutme.remove(user)
        
        # for each, look up their yji values, multiply it by their answer
        # and tally them all up
        tally = 0
        for otherguy in allbutme:
            tally = (tally +
                     yji[otherguy][subj][0] * yji[otherguy][subj][1])
    
        xij[subj][user][2] = tally

counter = 0
thous = 0

print "2A complete"

# 2B. update each yji
for user in yji:

    for subj in yji[user]:
        
        counter = counter + 1
        if counter == 1000:
            thous = thous + 1
            counter = 0
            print str(thous) + ",000 yji edges processed"

        # get all subjects other than the target subject
        allbutthis = yji[user].keys()
        allbutthis.remove(subj)

        # for each, look up its xij values, multiply it by its answer
        # and tally them all up
        tally = 0
        for othersubj in allbutthis:
            tally = (tally +
                     xij[othersubj][user][0] * xij[othersubj][user][2])

        yji[user][subj][2] = tally

print "2B complete"

#print xij["ASG000e402"]
#print
print yji[33856]
