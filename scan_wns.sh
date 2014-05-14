#!/bin/bash

echo "This will only work if you have root kerberos access to these nodes ..."
sleep 2
DATE=`date +%s`

mv cmsblah.txt  cmsblah.txt.${DATE} > /dev/null 2>&1

# wg

for n in `seq -w 0 9` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@wg0$n ". /vols/grid/cms_glexec.sh"; done >>  cmsblah.txt 2>&1

for n in `seq -w 10 69` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@wg$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

# we

for n in `seq -w 0 9` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@we00$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

for n in `seq -w 10 99` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@we0$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

# we115 and 116 are not in the cluster
for n in `seq -w 100 114` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@we$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

for n in `seq -w 117 119` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@we$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

# wf

for n in `seq -w 0 9` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@wf0$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

for n in `seq -w 10 35` ; do ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no root@wf$n ". /vols/grid/cms_glexec.sh"; done  >>  cmsblah.txt 2>&1

