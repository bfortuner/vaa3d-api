#!/bin/sh

echo "--> start.sh script running..."

echo "---> Starting circus..."
exec /usr/bin/circusd --daemon /home/ec2-user/vaa3d-api/circus.ini