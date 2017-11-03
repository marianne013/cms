#!/bin/bash

# assume a grid UI to be setup 
# lx00,01: source /cvmfs/grid.cern.ch/umd-sl6ui-test/etc/profile.d/setup-ui-example.sh
# lx02
# and a valid CMS proxy
# voms-proxy-init --voms cms

rm -rf gfal_files_not_found.txt
rm -rf check_files.log
rm -rf xrootd_barf.log

FILES=`cat lost_files.txt`

for f in $FILES
do
   echo -e "\nChecking file: " 
   echo $f
   FILE_TMP=${f##*/} # ain't stackoverflow great
   # can I list the file ?
   gfal-ls srm://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/${f}  >> check_files.log 2>&1
   if [ $? != 0 ]; then
       echo "File cannot be listed"
       # don't bother trying to copy it, but keep track of it
       echo "${f}" >> gfal_files_not_found.txt
       # can xrootd see it ?
       xrdcp -d3 root://cms-xrootd.gridpp.ac.uk/${f} $FILE_TMP  >> xrootd_barf.log 2>&1
       if [ $? != 0 ]; then
	   echo "No luck with xrootd either."
       else
	   echo "But xrootd can see it."
       fi
       rm -rf $FILE_TMP
       continue
   fi

   # now construct something gfal-copy will understand
   gfal-copy srm://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/${f} $FILE_TMP >> check_files.log 2>&1
   if [ $? != 0 ]; then
       echo "File copy failed"
       rm -rf $FILE_TMP
       continue
   fi
   FILE_SIZE=`du -sh ${FILE_TMP} | awk '{print $1}'`
   echo "File with size ${FILE_SIZE} successfully copied."
   rm -rf $FILE_TMP
   
   # now let's check xrootd
   xrdcp -d3 root://cms-xrootd.gridpp.ac.uk/${f} $FILE_TMP >> /dev/null 2>&1
   if [ $? != 0 ]; then
       echo "xrdcp failed!"
   else
       echo  "xrdcp success!"
   fi      
   rm -rf $FILE_TMP

done
