#!/usr/bin/env python3

import boto3
import os
import json


def set_retention(logGroupName, retentionInDays):
    client = boto3.client('logs')
    try:
        client.put_retention_policy(logGroupName=logGroupName, retentionInDays=retentionInDays, )
        print("Success")
        return "Success"
    except Exception as e:
        print("ERROR", e)
        return e

def lambda_handler(event, context):
    print(event)
    client = boto3.client('logs')

    production_retention_days = os.environ['production_retention_days'] 
    staging_retention_days = os.environ['staging_retention_days'] 
    develop_retention_days = os.environ['develop_retention_days'] 
    other_retention_days = os.environ['other_retention_days'] 
    print(production_retention_days, staging_retention_days, develop_retention_days, other_retention_days )

    log_group_name = event['detail']['requestParameters']['logGroupName']
    print(log_group_name)

    if 'production' in log_group_name:
        retention_days = production_retention_days
        set_retention(log_group_name, int(retention_days))
    elif 'staging' in log_group_name:
        retention_days = staging_retention_days
        set_retention(log_group_name, int(retention_days))
    elif 'develop' in log_group_name:
        retention_days = develop_retention_days
        set_retention(log_group_name, int(retention_days))
    else:
        retention_days = other_retention_days
        set_retention(log_group_name, int(retention_days))

    msg = "Set Retention to {} days for log Group {}".format( retention_days, log_group_name)
    print("Result", msg)

    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }
