#!/usr/bin/env python3

import boto3
import argparse

def get_log_group_names(logGroupNamePrefix):
	logGroupNames = []
	client = boto3.client('logs')
	paginator = client.get_paginator('describe_log_groups')

	for response in  paginator.paginate(logGroupNamePrefix=logGroupNamePrefix):
		for record in response['logGroups']:
			logGroupNames.append(record['logGroupName'])
	return logGroupNames

def set_retention(logGroupName, retentionInDays):
	client = boto3.client('logs')
	try:
		client.put_retention_policy(logGroupName=logGroupName, retentionInDays=retentionInDays)
		print("Success")
		return "Success"
	except Exception as e:
		print("Error", e)
		return e





if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--log_group_prefix", required=True, help="Log Group Name Prefix")
	parser.add_argument("-r", "--retention_days",required=True, help="Retention Days")

	args = parser.parse_args()
	log_prefix = args.log_group_prefix
	retention_days = args.retention_days
	log_groups = get_log_group_names(log_prefix)
	print(len(log_groups))
	for name in log_groups:
		set_retention(name, int(retention_days))
		print("Retention set to {} days for log group {}".format(retention_days, name))


