#!/bin/bash

# format stuff nicely
psx() {
    export PS_FORMAT=user:16,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,command; ps ax;
}

# format this differently

# echo -e "\n"
# echo "node: " `hostname`

# get a list of all the batch jobs on this node

BATHCJR=`ls -tr /srv/localstage/scratch`

NOW=`date +%s`

cd /srv/localstage/scratch

for JOB in $BATHCJR 
do

# this fails if the directory has disappared since the ls above
# ... at least that's what I think happens ...
    DIRAGE=`stat -c '%Z' ${JOB}`

# in this case, just ignore the directory, this will make it look very old     
    if [ -z "$DIRAGE" ]; then
	DIRAGE='0'
    fi

    # ignore all dirs older than 7 days
    TDIFF=$(( $NOW - $DIRAGE ))
    if [ $TDIFF -gt 600000 ]; then
        echo "Very old directory detected (${JOB}), you might want to perform some cleanup on " `hostname`
        continue
    fi

    # cmsplt jobs only
    DGROUP=`stat -c %G $JOB`
    if [ "${DGROUP}" != "lt2-cmsplt" ]; then
        continue
    fi

    # now I have the stuff I am looking for
    # try and find the matching job(s).
    # in principle there should be only one, but this is CMS

    CMSJOB=`psx | grep ${JOB} | grep cmsRun | grep -v "/usr/bin/time"`
    # the output typically looks like this:
    # glx-cms399 16639 98.3 5.7 1177876 933784 ? Rl 15:45:51 01:59:55 cmsRun -j /srv/localstage/scratch/4966592.1.grid.q/wiwKDm4ZM4jn3dFDVpGiSQRqaTsoMnABFKDmDKHKDmABFKDmaV0iin/glide_mbz2OC/execute/dir_14760/crab_fjr_1240.xml -p pset.py
    # check that this isn't empty to catch edge conditions
    if [ -z "$CMSJOB" ]; then
	echo "Sanity check: No cmsRun found for " ${JOB} " on " `hostname`
	# maybe those are pilot jobs as well and should go there ?
        continue
    fi



    # now extract the linux user it's running as and possible the project name and the DN
    # these commands only makes ssense when the job is actually running, not when the pilot 
    # job just hangs around

    # echo -e "\n"
    # echo "jobid: " $JOB

    # check if $CMSJOB is running (_condor_stdout should be present)
    ls ${JOB}/*/glide*/execute/dir*/_condor_stdout > /dev/null 2>&1

    if [ $? == 0 ]; then
	# occasionally there is more than one _condor_stdout
	sanitycheck=`ls ${JOB}/*/glide*/execute/dir*/_condor_stdout | wc -l`
#	echo $sanitycheck
	if [ $sanitycheck -gt 1 ]; then
	    echo "Sanity check: More that one _condor_stdout found for " ${JOB} " on " `hostname`
	    # leave this for now
	    continue
	fi    
        # get uid this job is using
        # echo "user: " `echo $CMSJOB | awk '{print $1}'`
	USERID=`echo $CMSJOB | awk '{print $1}'` 
        # get user DN - simple awk/print runs into trouble as DNs can have spaces
        # echo `grep subject ${JOB}/*/glide*/execute/dir*/_condor_stdout | tail -1`
	USERDN=`grep subject ${JOB}/*/glide*/execute/dir*/_condor_stdout | tail -1 |  cut -c13-`
        # get crab project, if available
	CRABPRJT=`grep CRAB_UNIQUE_JOB_ID ${JOB}/*/glide*/execute/dir*/_condor_stdout | awk '{print $6}'`
        # echo "crab project: " `grep CRAB_UNIQUE_JOB_ID ${JOB}/*/glide*/execute/dir*/_condor_stdout | awk '{print $6}'`
	# some jobs don't have crab projects for some reason
	# I don't know if this test works, as of course right now I only have well behaved crab jobs
	if [  -z "$CRABPRJT" ]; then
	    CRABPRJT="no_crab_project_id_found"
	fi    
    else
        # echo "pilot job only"
	USERID=`stat -c %U ${JOB}`   # returns the username of the owner of batchdir
	USERDN="pilot job only"
	CRABPRJT="pilotjob"
    fi

    # DN can consist of multiple fields, the rest is fixed, so I put it at the end
    echo `hostname` $JOB $USERID $CRABPRJT $USERDN 

done

