import os
import sys
import urllib.request
import ssl
import json

context = ssl._create_unverified_context()
f = open('result.txt','r')
encText = f.readline()
encText = encText.replace(' ', '%20')

url = 'https://apis.daum.net/search/web?apikey=d755bb7ac08c935267c72c2f2b0870be&q='+encText+'&output=json'
#url = 'https://apis.daum.net/search/web?apikey=d755bb7ac08c935267c72c2f2b0870be&q=weather&output=json'
request = urllib.request.Request(url)
response = urllib.request.urlopen(request, context=context)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    obj = json.loads(str(response_body.decode('utf-8')))
    print(response_body.decode('utf-8'))
    print(type(obj))

    print(obj['channel']['item'][0]['title'])
    print(obj['channel']['item'][0]['description'])
else:
    print("Error Code:" + rescode)