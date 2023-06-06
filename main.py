# This script export the code build log for a particular log group and stream


import boto3
from datetime import datetime, timedelta
import time
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--group', help='(required) : AWS Log group ', required=True, dest='group')
arg_parser.add_argument('--stream', help='(required) : AWS Log stream ', required=True, dest='stream')
arg_parser.add_argument('--outfile', help='(required) : Local file where logs will be downloaded ', required=True, dest='outfile')

cmdline_params = arg_parser.parse_args()

client = boto3.client('logs')

log_group = cmdline_params.group
latestlogStreamName = cmdline_params.stream
log_output_file = open(cmdline_params.outfile, "w")


response = client.get_log_events(
        logGroupName=log_group,
        logStreamName=latestlogStreamName,
        startFromHead=True,
    )
for x in range(len(response["events"])):
    print(response["events"][x]["message"], file=log_output_file)

while True:
    nextToken=response["nextForwardToken"]
    response = client.get_log_events(
        logGroupName=log_group,
        logStreamName=latestlogStreamName,
        nextToken=nextToken)
    for x in range(len(response["events"])):
        print(response["events"][x]["message"], file=log_output_file)
    if nextToken == response["nextForwardToken"]:
        break

log_output_file.close()
print(response)

