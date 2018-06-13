import urllib3
import json
import sys

#                       R E Q U I R E M E N T S
# 1. Requred Libraries : urllib3, json, sys. Ensure you pip install urlib3 json sys
# 2. An Instana Agent installed on the same machine where the script is executing.
#
#  First Parameter is the Query.
#  Script Fetch Traces in the past minute which contain an Error.
#  Count all of the Errors within the Trace
#  If Error is Greater Than ZERO Send Customer Event
#  For example:
#  querytraces.py trace.erroneous:true
#
#
#

traceQuery = "trace.erroneous:true"
base = "https://joe-joe.instana.io"
query = base + "/api/traces?windowsize=60000&sortBy=total_error_count&sortMode=asc&" + traceQuery
token = "XXXXXXXXXXXXXXXXX"


total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
# Pharsing args one by one
print ("Script name: %s" % str(sys.argv[0]))
print ("First argument is the Query: %s" % str(sys.argv[1]))

arguments = sys.argv
if len(arguments) > 1:
	query = arguments[1]
	traceQuery = query
elif len(arguments) <=1:
	traceQuery = "trace.errorCount:>0"


urllib3.disable_warnings()


print(query)

http = urllib3.PoolManager()
apirequest = http.request('GET', query, headers={'Authorization':'apiToken ' + token})
status = apirequest.status

#print(status)
jsonresultdata = json.loads(apirequest.data.decode('utf-8'))

ErrorCount = 0
TotalErrorCount = 0

tracelist = jsonresultdata.get("traces")
traceCount = len(tracelist)

traceCountStr = str(traceCount)
print("The Trace Count is " + traceCountStr)
print(tracelist)

for traceentry in tracelist[:]:
	errorCount = traceentry.get('errorCount')
	totalErrorCount = traceentry.get('totalErrorCount')
	ErrorCount = ErrorCount + int(errorCount)
	TotalErrorCount = TotalErrorCount + int(totalErrorCount)
	#print(id, " ", errorCount, " ", totalErrorCount, " ",  name, " ",  kind, " ", start, " ", duration, " ", batchSize)

if status == 200:
	print("# # # # # # #   API Result # # # # # # # ")
	print("The Trace Count is " + traceCountStr)
	print("Errors: " + str(ErrorCount))
	print("TotalErrorCount:  " + str(TotalErrorCount))
	print("Hello World")
	apirequest = http.request('POST', query, headers={'Authorization':'apiToken ' + token})
	print("# # # # # # #   Sending Custom Event # # # # # # # ")
	import json
	encoded_body = json.dumps({
			"title": "Custom API Events by Hugh Brien - hugh.brien@instana.com",
			"text": "This is Custom Event Generated as a result of a Trace Query",
			"duration": "1",
			"severity": "5",
		})

	http = urllib3.PoolManager()
	response = http.request('POST', 'http://localhost:42699/com.instana.plugin.generic.event',
					 headers={'Content-Type': 'application/json'},
					 body=encoded_body)
	results = response.read()
	print(response)

if status == 404:
	print ("No Results have returned")

