# Amazon Linux Base Image
FROM public.ecr.aws/amazonlinux/amazonlinux:latest

# Install updates and Python/Pip
RUN yum update -y
RUN yum install python3 python-pip -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install boto3 six

# Install ClamAV and run initial update
RUN yum install amazon-linux-extras -y
RUN PYTHON=python2 amazon-linux-extras install epel -y
RUN yum install -y gcc gcc-c++ clamav clamd clamav-update
#RUN freshclam

# Install the AWS CLI tools and set default region to us-gov-west-1
RUN yum install unzip -y
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN aws configure set region us-gov-west-1

# Copy virus scanner python to Lambda /tmp directory
COPY *.py /tmp/
COPY *.sh /tmp/

# Change working directory to /tmp
WORKDIR /tmp

# ENTRYPOINT [ "python3", "/tmp/virus-scanner.py", "{\"requestParameters\": {\"bucketName\" : \"virusscanner\", \"key\" : \"tainted.txt\"}}" ]
ENTRYPOINT [ "sh", "/tmp/initialize.sh" ]



### Previous code - for reference

# Sync latest defintions from S3 - run virus scan on file
#CMD aws s3 sync s3:///<<INSERT_BUCKET_NAME_HERE>> /var/lib/clamav/ && python3 /tmp/virus-scanner.py

# ## Configure Local ClamAV Updates
# RUN pip3 install cvdupdate
# RUN cvd config set --dbdir https://<<INSERT_BUCKET_NAME_HERE>>.s3-us-gov-west-1.amazonaws.com/
# #RUN cvd update

# COPY *.sh /tmp/
