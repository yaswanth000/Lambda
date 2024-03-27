import boto3
import json
import os
emr = boto3.client('emr')
cloudwatch = boto3.client('cloudwatch')
s3 = boto3.resource('s3')
cloudwatchRes = boto3.resource('cloudwatch')
metric = cloudwatchRes.Metric('namespace', 'name')
paginator = cloudwatch.get_paginator('list_metrics')
emr = boto3.client('emr')
cloudwatch = boto3.client('cloudwatch')
s3 = boto3.resource('s3')
def lambda_handler(event, context):
  clusterId=event['clusterId']
  cloudwatch.delete_dashboards(DashboardNames=[clusterId])
  print(clusterId)
  return clusterId
