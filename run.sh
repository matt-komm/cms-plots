#!/bin/bash
source /nfs/home/fynu/mkomm/.bashrc
env
cd /nfs/user/mkomm/stpol_step3/cms-plots
pwd
python condor.py $@

