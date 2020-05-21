import urllib.request
import json
import os
import ssl
import flask

f = open("response.json", "w")



def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

data = {
    "Inputs": {
          "WebServiceInput0":
          [
              {
                    'Datetime': "2020-05-21T03:26:00Z",
                    'Open': "185.03",
                    'High': "186",
                    'Low': "184.7",
                    'Close': "184.91"
              },
          ],
    },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))

url = 'http://13.86.60.147:80/api/v1/service/regression-model-real-time-infer/score'
api_key = 'ruN30ABYnhqgziksjMh8h86lhxPx1OhA' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    res_json=result.decode('utf-8')
    f.write(res_json)
    print(res_json)
    
    
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))

f.close()