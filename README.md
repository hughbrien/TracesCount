
# TracesCount

Script Fetch Traces in the past minute which contain an Error.

* Requred Libraries : urllib3, json, sys. Ensure you pip install urlib3 json sys
* __An Instana Agent installed on the same machine where the script is executing__.

* First Parameter is the Query.
* Script Fetch Traces in the past minute which contain an Error.
* Count all of the Errors within the Trace
* If Error is Greater Than ZERO Send Customer Event
* For example:
* querytraces.py trace.erroneous:true

# Need to update these items
* traceQuery = "trace.erroneous:true"
* base = "https://joe-joe.instana.io"
* query = base + "/api/traces?windowsize=60000&sortBy=total_error_count&sortMode=asc&" + traceQuery
* token = "XXXXXXXXXXXXXXXXX"
