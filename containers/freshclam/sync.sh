#!/bin/ash

set -e

export AWS_ACCESS_KEY_ID=$KEY
export AWS_SECRET_ACCESS_KEY=$SECRET
export AWS_DEFAULT_REGION=$REGION

echo "$(date) - Start"

aws s3 sync /var/lib/clamav s3://$BUCKET$BUCKET_PATH $PARAMS

echo "$(date) End"
