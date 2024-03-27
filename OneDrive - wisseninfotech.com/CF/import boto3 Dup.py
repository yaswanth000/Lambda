import boto3
 
def lambda_handler(event, context):
    # Initialize CloudWatch client
    cloudwatch = boto3.client('cloudwatch')
 
    # Get all alarms
    response = cloudwatch.describe_alarms()
 
    # Initialize a dictionary to store alarm names and their configurations
    alarm_configs = {}
 
    # Iterate through each alarm
    for alarm in response['MetricAlarms']:
        alarm_name = alarm['AlarmName']
        alarm_configuration = alarm['MetricName']  # You may want to adjust this based on your criteria
        
        # Check if alarm configuration already exists
        if alarm_configuration in alarm_configs:
            # Delete duplicate alarm
            cloudwatch.delete_alarms(AlarmNames=[alarm_name])
            print(f"Duplicate alarm '{alarm_name}' deleted.")
        else:
            # Add alarm configuration to dictionary
            alarm_configs[alarm_configuration] = alarm_name
 
    return {
        'statusCode': 200,
        'body': 'Duplicate alarms removed successfully.'
    }