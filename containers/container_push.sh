# Create ECR (if not already existing)

AWS_REGION=$(aws configure get region --profile default)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
#$(aws ecr get-login --no-include-email --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com)
$(aws ecr get-login --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com)

docker build -t virusscanner ./clamav/
docker tag virusscanner:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/virusscanner:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/virusscanner:latest

docker build -t clamavdefs ./freshclam/
docker tag clamavdefs:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/clamavdefs:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/clamavdefs:latest
