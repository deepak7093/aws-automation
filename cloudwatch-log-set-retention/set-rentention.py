#!/usr/bin/env python3

import boto3
import argparse

def get_log_group_names(logGroupNamePrefix):
	log_groups_names = []
	response = client.describe_log_groups(logGroupNamePrefix=logGroupNamePrefix, limit=50)
	for record in response['logGroups']:
		log_groups_names.append(record['logGroupName'])
	return log_groups_names

def set_retention(logGroupName, retentionInDays):
	try:
		client.put_retention_policy(retentionInDays, logGroupName)
		return "Success"
	except Exception:
		return Exception





if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--log_group_prefix", required=True, help="Log Group Name Prefix")
	parser.add_argument("-r", "--retention_days",required=True, help="Retention Days")

	args = parser.parse_args()

	client = boto3.client('logs')
	log_prefix = args.log_group_prefix
	retention_days = args.retention_days
	log_groups = get_log_group_names(log_prefix)
	for name in log_groups:
		set_retention(name, retention_days)
		print("Retention set to {} days for log group {}".format(retention_days, name))


