# import-EVTX-to-XDR
short python script to convert, enrich and upload an EVTX file to Cortex XDR using an HTTP Custom Collector

First, you need to connect to your Cortex XDR console and create a new HTTP Custom Collector. It'll generate a token key you will need to add in the api_key variable of the script.
Then, you need to specify the api_url you could also get from the Cortex XDR console by clicking on "Copy api url" button of your Custom Collector.

Finally, you could simply run the script:
$ python3 ./import_evtx_file_to_XDR_0.8.py tests/security-win10-May3rd.evtx 
