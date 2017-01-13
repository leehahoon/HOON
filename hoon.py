from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sys
import urllib.request
import urllib.parse
import ssl
import json

UPLOAD_FOLDER = 'sst/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ogg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/hoon', methods=['GET', 'POST'])
def soonsil():
	if request.method == 'GET':
		return render_template('hoon.html')

	else:
		file = request.files['audio-blob']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		os.system('sst/speech2text.sh')
		return redirect(url_for('results'))

@app.route('/results', methods=['GET', 'POST'])
def results():
	context = ssl._create_unverified_context()
	f = open('sst/result.txt','r')
	encText = f.readline()
	encText = encText.replace(' ', '%20')
	encText = urllib.parse.quote(encText)

	url = 'https://apis.daum.net/search/web?apikey=d755bb7ac08c935267c72c2f2b0870be&q='+encText+'&output=json'
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request, context=context)
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read()
		obj = json.loads(str(response_body.decode('utf-8')))
	else:
		print("Error Code:" + rescode)
	text=urllib.parse.unquote(encText)

	return render_template('results.html', obj=obj, text=text)

if __name__ == '__main__':
	app.run(port=1828, debug=True, host='0.0.0.0')