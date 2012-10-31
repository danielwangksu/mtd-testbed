#!/bin/sh
###################################################################
# Purpose: Install git and pull down kickstarter stage2
# Author: Ian Unruh
###################################################################
set -e

PATH=/bin:/sbin:/usr/sbin:/usr/bin
KSPATH=/tmp/ks

## Install git
apt-get update
apt-get install -y git

## Pull down kickstarter stage2
git clone git://github.com/iunruh/mtd-kickstart.git $KSPATH && cd $KSPATH
sh ks-stage2.sh