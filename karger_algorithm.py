#!/usr/bin/python

import csv
import random
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

#filename = "season4.csv"
filename = "fakedata.csv"

species = 47 # wildebeest

k = 30 # iterations

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
            arrlist = [-1,0] + [0]*k
            xij[subj][user] = array('f',arrlist)
        
        # create a dictionary for each user in yji
        if not yji.has_key(user):
            yji[user] = dict()

        # create and array for each user-capture
        if not yji[user].has_key(subj):
            startnum = random.gauss(1,1)
            arrlist = [-1] + [startnum] + [0]*k
            yji[user][subj] = array('f',arrlist)

        # and note that it's 1 if that animal was seen
        if spp==species:
            xij[subj][user][0] = 1
            yji[user][subj][0] = 1

        # just keep track of how many there are to do
        total = total + 1

print "total of " + str(total) + " lines read\n"

# now we do the algorithm.
# 1. we already initialized all users to have reliability 1

# iterate
for m in range(1,k+1):
    print "iteration " + str(m)
    
    counter = 0
    thous = 0

    # 2A. update each xij
    for subj in xij:

        # for efficiency, calculate the sum of answer * yji for all users
        # O(N) instead of O(N^2)
        tally = 0
        for eachuser in xij[subj].keys():
           tally = (tally +
                    yji[eachuser][subj][0] * yji[eachuser][subj][m])

        numusers = len(xij[subj].keys())    

        # and then do each user's score
        for user in xij[subj]:

            counter = counter + 1
            if counter == 100000:
                thous = thous + 1
                counter = 0
                print str(thous) + "00,000 xij edges processed"

            # case where subject has been done just one user? this shouldn't happen
            if numusers == 1:
                xij[subj][user][m+1] = 0
                print xij[subj]
            else:
                # subtract out the current user and divide
                xij[subj][user][m+1] = ((tally -
                                      (yji[user][subj][0] * yji[user][subj][m]))/
                                      (numusers-1))


    counter = 0
    thous = 0

    print "2A complete"
    
    # 2B. update each yji
    for user in yji:

        # for efficiency, calculate the sum of answer * xij for all subjects
        # O(N) instead of O(N^2)
        tally = 0
        for eachsubj in yji[user].keys():
           tally = (tally +
                    xij[eachsubj][user][0] * xij[eachsubj][user][m+1])

        numsubjs = len(yji[user].keys())

        # and then do each subject's score
        for subj in yji[user]:
        
            counter = counter + 1
            if counter == 100000:
                thous = thous + 1
                counter = 0
                print str(thous) + "00,000 yji edges processed"

            # case where user has done just one subject
            if numsubjs == 1:
                yji[user][subj][m+1] = 0
            else:
                # subtract out the current subject
                yji[user][subj][m+1] = ((tally -
                                      (xij[subj][user][0] * xij[subj][user][m+1]))/
                                      (numsubjs-1))

    print "2B complete"


# 3. and calculate answers
with open("output.csv",'w') as fh:

    fwriter = csv.writer(fh, delimiter=',')
    fwriter.writerow(["zoonID"])
        
    # for each subject
    for subj in xij:

        outarr = array('f',[0]*k)        

        # for each iteration
        for m in range(1,k+1):

            # tally the sum of each user's answer multiplied by their score
            tally = 0
            for eachuser in xij[subj].keys():
               tally = (tally +
                        yji[eachuser][subj][0] * yji[eachuser][subj][m+1])

            outarr[m-1] = tally

        # wildebeest
        wildebeest = False
        if outarr[k-1]>0:
            wildebeest = True

        fwriter.writerow([subj]+list(outarr)+[wildebeest])



