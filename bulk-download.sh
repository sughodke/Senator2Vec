#!/bin/bash

# Using GovTrack's bulk download service to get 
# all senate and house of representative votes 
# on bills proposed.

# This script should be modified to download only
# those sessions of congress you are interested
# in. (If you want just one session of congress
# set the ID and issue the below rsync command,
# e.g. ID=112)

# Note that data may not be available for <96th
# session of congress

set -x

pushd congress

for ID in {97..99}
do
  rsync -avz --delete --delete-excluded \
    --exclude **/text-versions/ \
    --exclude *xml \
    govtrack.us::govtrackdata/congress/$ID/votes votes-$ID
done

popd
