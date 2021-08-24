#!/bin/bash

aws s3 sync s3://<<INSERT_BUCKET_NAME_HERE>> /var/lib/clamav/
python3 /tmp/virus-scanner.py
