### Build this Dockerfile with the name clamdefs
## Additionally, change the S3 bucket name to your desired S3 bucket

# Amazon Linux Base Image
FROM public.ecr.aws/amazonlinux/amazonlinux:latest

# Install ClamAV and run freshclam to update virus definitions
RUN yum update -y 
RUN amazon-linux-extras install epel
RUN yum install clamav clamd -y
RUN freshclam

# Install the AWS CLI tools
RUN yum install unzip -y
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Set AWS default region as us-gov-west-1
# Should be set to the AWS region where the S3 bucket resides
RUN aws configure set region us-gov-west-1

# Run freshclam and sync results to S3
CMD freshclam && aws s3 sync /var/lib/clamav/ s3://<<INSERT_BUCKET_NAME_HERE>>/
