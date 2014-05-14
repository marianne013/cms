#!/usr/bin/python -tt 

import string
import getopt
import sys

# stolen from stackoverflow
# used to find the fifth '_' in the crab id
def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def print_help():
    print "Usage:"
    print "cms_user.py -h: print this help"
    print "cms_user.py [no arguments]: prints overview"
    print "cms_user.py -w [wnname]: prints all info for given WN"
    print "cms_user.py -r: prints raw data (debugging option)"
    print "cms_user.py -o [wn/dn/crabid] - one argument only, please"
    print "cms_user.py expects cmsblah.txt as input"
def main(argv):
    
    
    wnonly='' # if set, print information for this WN only
    print_this_overview='' # if in doubt print all possible overviews (dn/wn/prj)
    print_raw_data=False
   
    # arguments are: -h (help), -r rawdata, -w (workernode, needs argument)
    # -o type of overview to print (needs argument)
    try:
        opts, args = getopt.getopt(argv,"hrw:o:") 
        
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
        
      
      # if no arguments, this loop is never entered, hence no 'else' required    
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit(0)
        elif opt == '-w': 
            wnonly = arg
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
     # for debugging    
    if print_raw_data == True:     
        for line in rawdata:    
            print line

    # read all jobs into a list
    # jobs are stored as tuples (jobid, wn, userid, crabid, dn)
    cmsjobs = []   # list
    with open("cmsblah.txt") as rawfile:
        data = [line.split() for line in rawfile]
    for line in data:
        # print line[0],  line[1],  line[2],  line[3]
        # print len(line)
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

    # print jobs for selected WN only
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

    # generate overview: number of jobs per WN/DN/CRABID
    if wnonly == '':    
        jobs_per_wn = {} # ohh dictionary        
        jobs_per_dn = {}
        jobs_per_crabid = {}
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
                
            if crabid not in jobs_per_crabid:
                jobs_per_crabid[crabid] = 1
            else:
                jobs_per_crabid[crabid] =  jobs_per_crabid[crabid]+1

        
        # now loop over the result
        if print_this_overview == '' or print_this_overview == 'wn':
            print "\n***Listing number of CMS user jobs by WN"
            for wn,n_of_jobs in sorted(jobs_per_wn.iteritems()):        
                print wn, n_of_jobs

        if  print_this_overview == '' or print_this_overview == 'dn':
            print "\n***Listing number of CMS user jobs by DN"
            for dn,n_of_jobs in sorted(jobs_per_dn.iteritems()):
                print dn, n_of_jobs

        if  print_this_overview == '' or print_this_overview == 'crabid':
            print "\n***Listing number of CMS user jobs by CRABID"
            for crabid,n_of_jobs in sorted(jobs_per_crabid.iteritems()):
                print crabid, n_of_jobs

   
    

    
if __name__ == '__main__':
    main(sys.argv[1:])
