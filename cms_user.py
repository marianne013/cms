#!/usr/bin/python -tt 

import string
import getopt
import sys

# stolen from stackoverflow
# used to find the fifth '_' in the crab id
def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def main(argv):
    
    
    wnonly='' # testing on an empty string not ideal
    print_this_overview='' # if in doubt print wn and dn
    print_raw_data=False
    try:
        opts, args = getopt.getopt(argv,"hrw:o:") # arguments -h for 'help' , -w for 'worker node'
        
    except getopt.GetoptError:
        print 'basic_text.py [-w name_of_workernode]'
        sys.exit(2)
        
      # if no arguments, this loop is never entered, hence no 'else' required    
    for opt, arg in opts:
        if opt == '-h':
            print 'basic_text.py [-w name_of_workernode]'
        elif opt == '-w': 
            wnonly = arg
            # print 'Looking at '+wnonly
        elif opt == '-r':
            print 'Printing raw data'
            print_raw_data=True
        elif opt == '-o':
            print_this_overview=arg # can be 'wn' or 'dn' 
        # else:
         #   print 'no argument given, printing overview'
    

    #  open file
    with open("cmsblah.txt") as rawfile:
        rawdata= rawfile.readlines()
        # rawdata.read().splitlines()
    if print_raw_data == True:     
        for line in rawdata:    
            print line

    cmsjobs = []   # list
    with open("cmsblah.txt") as rawfile:
        data = [line.split() for line in rawfile]
    for line in data:
        # print line
        # print line[0],  line[1],  line[2],  line[3]
        # print len(line)
     
        # make a tuple
        # this is jobid, wn, userid, crabid, dn
        # exclude debugging line ('Very old directory ...')
        # and jobs that failed the Sanity check
        if line[0] != 'Very' and line[0] != 'Sanity':
            # reassemble the DN with all spaces
            dn=line[4]+' '
            for i in range (5, len(line)):
                dn=dn+line[i]
                if i < (len(line)):
                    dn=dn+' '
            # crab ids have random numbers at the end, but also seem
            # to have no fixed length
            # cut of everything from the fourth last '_' for some cleanup
            # exclude jobs where no crabid was found
            crabidtmp=line[3]
            if  crabidtmp != 'no_crab_project_id_found':
                crabidunder=findOccurences(line[3], '_')    
                # print crabidunder
                if len(crabidunder) > 0:
                    # print crabidunder[len(crabidunder)-3]
                    # print line[3]
                    crabidtmp=line[3][0:crabidunder[len(crabidunder)-4]]
                    # print crabidtmp
            
                
            job=(line[1],  line[0],  line[2], crabidtmp, dn)
            cmsjobs.append(job)


    if wnonly != '':
        # print 'All jobs for '+wnonly
        jobsonthiswn=[]
        for jobid, wn, userid, crabid,dn in cmsjobs:
            if wn == wnonly:
                wjob=(jobid,userid,crabid,dn)
                # make a list, so I can sort the output
                jobsonthiswn.append(wjob)
                
        jobsonthiswn.sort(key=lambda x : x[2]) # sort list by crab project
        # format nicely
        for jobid, userid, crabid,dn in jobsonthiswn:
             print jobid+': '+userid+'\t'+crabid+'\t'+dn+'\n'         

    # no arguments given, print overview
    if wnonly == '':
        jobs_per_wn = {} # ohh dictionary        
        jobs_per_dn = {}
        for jobid, wn, userid, crabid,dn in cmsjobs:
            # print wn
            # count the number of jobs by WN
            # this should be a function and there's probably a clever way in python to do this
            if wn not in jobs_per_wn:
                jobs_per_wn[wn] = 1
            else:
                jobs_per_wn[wn] = jobs_per_wn[wn]+1
    
            if dn not in jobs_per_dn:
                jobs_per_dn[dn] = 1
            else:
                jobs_per_dn[dn] = jobs_per_dn[dn]+1


        
        # now loop over the result
        if print_this_overview == '' or print_this_overview == 'wn':
            for wn,n_of_jobs in sorted(jobs_per_wn.iteritems()):        
                print wn, n_of_jobs

        if  print_this_overview == '' or print_this_overview == 'dn':   
            for dn,n_of_jobs in sorted(jobs_per_dn.iteritems()):
                print dn, n_of_jobs



   
    

    
if __name__ == '__main__':
    main(sys.argv[1:])
