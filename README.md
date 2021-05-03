# import-EVTX-to-XDR
short python script to convert, enrich and upload an EVTX file to Cortex XDR using an HTTP Custom Collector

Here is the typical way to use the script:
$ python3 ./import_evtx_file_to_XDR_0.8.py tests/security-win10-May3rd.evtx 
---------------------------------------------
- CORTEX XDR EVTX file importer script v0.8 -
---------------------------------------------

INFO - DEBUG mode ON
INFO - 421 entries in the eventID mapping table
INFO - EVTX file tests/security-win10-May3rd.evtx analysis in progress
INFO - 25268 events included in this EVTX file
INFO - Import started at 2021-05-03 17:41:00 with 2000 events per API call

INFO - API POST #1 including 2000 events / payload size: 3254.4 KB / 2000 events uploaded out of 25268 - 7.92% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #2 including 2000 events / payload size: 3245.7 KB / 4000 events uploaded out of 25268 - 15.83% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #3 including 2000 events / payload size: 3059.0 KB / 6000 events uploaded out of 25268 - 23.75% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #4 including 2000 events / payload size: 3217.2 KB / 8000 events uploaded out of 25268 - 31.66% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #5 including 2000 events / payload size: 3242.0 KB / 10000 events uploaded out of 25268 - 39.58% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #6 including 2000 events / payload size: 3275.5 KB / 12000 events uploaded out of 25268 - 47.49% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #7 including 2000 events / payload size: 3280.9 KB / 14000 events uploaded out of 25268 - 55.41% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #8 including 2000 events / payload size: 3298.4 KB / 16000 events uploaded out of 25268 - 63.32% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #9 including 2000 events / payload size: 3303.4 KB / 18000 events uploaded out of 25268 - 71.24% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #10 including 2000 events / payload size: 3306.1 KB / 20000 events uploaded out of 25268 - 79.15% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #11 including 2000 events / payload size: 3314.8 KB / 22000 events uploaded out of 25268 - 87.07% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #12 including 2000 events / payload size: 3229.9 KB / 24000 events uploaded out of 25268 - 94.98% / return code:  <Response [200]> / return output: {"error":"false"}
INFO - API POST #13 including 1268 events / payload size: 2048.1 KB / 25268 events uploaded out of 25268 - 100.00% / return code:  <Response [200]> / return output: {"error":"false"}

INFO - Import finished at 2021-05-03 17:41:25
INFO - EVTX import in XDR performed with success: 25268 events imported in 0:00:24.672240 (hh:mm:ss) at 1052.83 events/second.
---------------------------------------------
