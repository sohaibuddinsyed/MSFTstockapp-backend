# This file contains all the routes for our application. This will tell Flask what to display on which path.

import urllib.request
import json
import os
import ssl
import flask
import json
from datetime import datetime, timedelta
import yfinance as yf

#access to blob storage
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

#flask imports
from flask import render_template
from app import app
from flask import request, redirect

formresponse= {
    'Datetime':'',
    'Open':'',
    'High':'',
    'Low':'',
    'Close':'',
    'Option':''
}

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.




url = 'http://13.86.60.147:80/api/v1/service/regression-model-real-time-infer/score'
api_key = 'ruN30ABYnhqgziksjMh8h86lhxPx1OhA' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}


@app.route('/', methods=['GET','POST'])
def index(): 

    #response list from server
    resultlist= ['','','','','','']
    #current values from yfinance (also has adj close and volume)
    latest_values= ['','','','','','']
    marketopen=None
    custominput=None
    
    if request.method == 'POST':
        
        #Downloads fresh DB from yfinance
        x=datetime.now()
        date_N_days_ago = datetime.now() - timedelta(days=7)
        msft = yf.Ticker("MSFT")
        data_df = yf.download("MSFT", start=date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d"), interval="1m", end=x.strftime("%Y"+"-"+"%m"+"-"+"%d"))
        # data_df= yf.download("MSFT",start="2000-01-01",end="2006-01-01")
        data_df.to_csv('ds.csv')

        #updates blob
        try:
            # print("Azure Blob storage v12 - Python quickstart sample")
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            # print(connect_str)
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Create a unique name for the container
            container_name = "datasetcontainer" 

            # Create the container
            # container_client = blob_service_client.create_container(container_name)
            # Create a file in local data directory to upload and download
            local_path = "./"
            local_file_name = "ds.csv"
            upload_file_path = os.path.join(local_path, local_file_name)


        # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
            # Instantiate a ContainerClient
            container_client = blob_service_client.get_container_client("datasetcontainer")
            container_client.delete_blob("ds.csv")

            print("\nDeleting blob from Azure Storage:\n\t" + local_file_name)

            print("\n\n Now, uploading to Azure Storage as blob:\n\t" + local_file_name)
        
        # Upload the created /file
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)
        
        except Exception as ex:
            print('Exception:')
            print(ex)
   


        #fetches response from the user
        formresponse["Datetime"]=request.form["datetime"]
        formresponse['Open']=request.form["open"]
        formresponse['High']=request.form["high"]
        formresponse['Low']=request.form["low"]    
        formresponse['Close']=request.form["close"]
        formresponse['Option']=request.form["option"]
        

        print(formresponse['Datetime'])
        print(formresponse['Open'])
        print(formresponse['High'])
        print(formresponse['Low'])
        print(formresponse['Close'])

                
        with open("ds.csv", "r") as file:
            first_line = file.readline()
            for last_line in file:
                pass
        latest_values=last_line.split(',')
        print(latest_values[1])
        
        usa_time=((latest_values[0].split())[1].split('-'))[0]
       
        if usa_time > str("09:00:00") and usa_time < str("16:00:00") :
            latest_values[5] = "Market Open. Showing current trends at "+usa_time+" NY local time."
        else:
           latest_values[5] = "Market Closed. Showing MSFT stock values from last closing on "+(latest_values[0].split())[0]+" at "+usa_time+" NY local time."
        
        marketopen = (usa_time > str("09:00:00") and usa_time < str("16:00:00"))
        if  marketopen == False:
            marketopen=None
        # latest_datetime=latest_values[0]
        # latest_open=latest_values[1]
        # latest_high=latest_values[2]
        # latest_low=latest_values[3]
        # latest_close=latest_values[4]
        if request.form["option"] == "yes":
            custominput=None
            data = {
                "Inputs": {
                    "WebServiceInput0":
                    [
                        {
                                'Datetime':formresponse['Datetime'],
                                'Open':  latest_values[1],
                                'High': latest_values[2],
                                'Low': latest_values[3],
                                'Close': latest_values[4]
                        },
                    ],
                },
                "GlobalParameters":  {
                }
            }
        else:
            data = {
                "Inputs": {
                    "WebServiceInput0":
                    [
                        {
                                'Datetime': formresponse['Datetime'],
                                'Open': formresponse['Open'],
                                'High': formresponse['High'],
                                'Low': formresponse['Low'],
                                'Close': formresponse['Close']
                        },
                    ],
                },
                "GlobalParameters":  {
                }
            }

        body = str.encode(json.dumps(data))
        
        req = urllib.request.Request(url, body, headers)
        
        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            res_json=result.decode('utf-8') 
            y = json.loads(res_json)

            # the result is a Python dictionary:
            a=y['Results']['WebServiceOutput0']
            b=a[0]
            resultlist=[b["Datetime"],b["Open"],b["High"],b["Low"],b["Close"],b["Scored Labels"]]

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))

              
    return render_template("index.html", currentdatetime=datetime.now().strftime("%d %B, %Y at %I:%M %p") ,preddatetime=resultlist[0], open= resultlist[1], high= resultlist[2], low= resultlist[3], close= resultlist[4], prediction= resultlist[5], currentopen=latest_values[1], currenthigh=latest_values[2], currentlow=latest_values[3], current_close=latest_values[4], marketnow=latest_values[5], marketopenview=marketopen, custominput=custominput)



@app.route('/about')
def about():
    return render_template("about.html")
