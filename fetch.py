from flask import Flask
from flaskext.mysql import MySQL
import requests
from pprint import pprint
import json
from os import listdir, walk
import time

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'mapliv'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'mapliv'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def getBounds():
	#it's buttomLeft and topRight actually
	topLeft = [49.001654, -123.286894]
	bottomRight = [49.360108, -122.712711]
	row = 3
	column = 3
	stepColumn = (topLeft[1]-bottomRight[1])/column
	stepRow = (topLeft[0]-bottomRight[0])/row
	rowList = [str(topLeft[0])]
	columnList = [str(topLeft[1])]
	tmp = topLeft[0]
	for i in range(column):
		tmp -= round(stepRow, 6)
		rowList.append(str(tmp))
	tmp = topLeft[1]
	for i in range(row):
		tmp -= round(stepColumn, 6)
		columnList.append(str(tmp))
	bounds = []
	for i in range(column):
		for j in range(row):
			bounds.append(rowList[i]+','+columnList[j]+','+rowList[i+1]+','+columnList[j+1])
	return bounds
	


def init():
	f = []
	bounds = getBounds()
	request_data = {'zoom':13, 'pmin':0, 'pmax':20000, 'bed_min':0, 'bed_max':5, 'post_date':50, 'bounds': '49.207014,-123.379174,49.31248,-122.805996', 'capacity': 2000}
	prefix = time.strftime("%Y_%m_%d");
	for bound in bounds:
		request_data['bounds'] = bound
		index = '0'
		for filename in listdir('./files'):
			lst = filename.split('-')
			if (len(lst)>=2 and lst[0] == prefix):
				index = str(max(int(lst[1])+1, int(index)))
		f = open('./files/'+prefix+'-'+index, 'w')
		r = requests.post('http://mapliv.com/fetch_data.php', data=request_data)
		data = r.json()
		json.dump(data, f)
 
# @app.route("/")
# def hello():
#     return "Welcome to Python Flask App!"

if __name__ == "__main__":
    init()
