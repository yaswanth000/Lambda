import boto3

def lambda_handler(event, context):
    # Create EC2 client
    ec2 = boto3.client('ec2')
    
    # Call describe_instances() to get information about all instances
    response = ec2.describe_instances()
    
    # Iterate over reservations to extract instance details
    running_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Check if the instance state is 'running'
            if instance['State']['Name'] == 'running':
                instance_details = {
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'State': instance['State']['Name']
                }
                running_instances.append(instance_details)
    
    # Return the list of running instances
    return running_instances
