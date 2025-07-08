import boto3

region = 'us-east-1'  # Remplace par ta région AWS
instances = ['i-0123456789abcdef0']  # Remplace par l’ID de ton instance EC2
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('Stopped your instances: ' + str(instances)) 
