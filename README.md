# import-EVTX-to-XDR
This file is a short python script to convert, enrich and upload an EVTX file to Cortex XDR using an HTTP Custom Collector. Cortex XDR requires a Pro per TB license to ingest such information. All the fields of the EVTX file will be represented in Cortex as a flat JSON key/value structure with underscores between elements of the original EVTX structure. 

## Configuration is easy
1. Connect to your Cortex XDR console in Settings to create a new HTTP Custom Collector. Please select "uncompressed" and "JSON" Log Format.
2. Copy/Paste the displayed token key to the the api_key variable of the script.
3. Copy/Paste the API URL displayed by clicking on "copy api url" to the api_url variable of the script.
4. Finally, you could simply run the script:
```
$ python3 ./import_evtx_file_to_XDR_0.8.py tests/security-win10-May3rd.evtx 
```

## EventID enrichement
Go to Investigation / Query Builder and start an XQL Search query. Simply query the dataset you just created and type "eventid" in the search fields. Windows EventID will be available in the **Event_System_EventID** while the enriched full text name will be available in **Event_System_EventID_Name**. In addition, **Event_System_EventID_Type** represents the EventID type like Policy Change, Process Tracking...
Using Event_System_EventID_Type is an easy to start looking for anomalies.
