#!/usr/bin/python
#
'''
    File name: ip_label_request.py
    License: GNU LESSER GENERAL PUBLIC LICENSE
    Author: Kevin Chollet @ Net4all
    Date created: 11/04/2018
    Date last modified: 16/04/2018
    Python Version: 2.7.3 | 3.2.3
'''

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import argparse

parser = argparse.ArgumentParser(description='IP label check')

parser.add_argument('-u', '--username',
    action="store", dest="username",
    help="IPLabel Username", required=True)

parser.add_argument('-p', '--password',
    action="store", dest="password",
    help="IPLabel Password", required=True)

parser.add_argument('-o', '--orange',
    action="store", dest="orange",
    help="Enable warning on orange state", default="true", choices=['false', 'true'])

parser.add_argument('-r', '--red',
    action="store", dest="orange",
    help="Enable warning on red state", default="true", choices=['false', 'true'])

parser.add_argument('-f', '--filter',
    action="store", dest="filter",
    help="Add filter on monitor")

options = parser.parse_args()

url_alarms = "https://ws.ip-label.net/REST/Get_Current_Alarms_All_Monitors/"
url_monitors = "https://ws.ip-label.net/REST/Get_Monitors/"

auth=HTTPBasicAuth(options.username, options.password)

alarms = requests.get(url_alarms,auth=auth)
monitors = requests.get(url_monitors,auth=auth)

json_monitors = json.loads(monitors.content);
monitor_list = json_monitors["Ipln_WS_REST_datametrie"]["Get_Monitors"];
display_name={};
for key in monitor_list :
	if key != "status" :
		display_name[monitor_list[key]["IDCONTRAT"]] = monitor_list[key]["NOMCONTRAT"];

alarms_data = json.loads(alarms.content);
alert_list = alarms_data["Ipln_WS_REST_datametrie"]["Get_Current_Alarms_All_Monitors"];

return_code=0
for key in alert_list:
	if key != "status" :
		if options.filter == "" or display_name[alert_list[key]["IDCONTRAT"]] == options.filter:
			if alert_list[key]["TYPEALARME"] == "ORANGE" and return_code<2 and options.orange == "true":
				return_code=1
			elif alert_list[key]["TYPEALARME"] == "RED" and return_code<2 and options.red == "true":
				return_code=1
			elif alert_list[key]["TYPEALARME"] == "BLACK":
				return_code=2
			print("Alert %s on monitor %s" % (alert_list[key]["TYPEALARME"], 
display_name[alert_list[key]["IDCONTRAT"]]))

sys.exit(return_code);

