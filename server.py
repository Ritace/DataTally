from sqlalchemy import *
#database conntection settings table as datatable
from db_conn import *
from flask import Flask, request
import json

app = Flask(__name__)
null = False;
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/district")
def district():
	
	querystr = request.args.get('dist')
	print(querystr)
	stmt = "select distinct fld_HI_Name,fld_HI_SID from DataTable where fld_Dist_NM = '" + querystr + "';"
	print(stmt)
	result = conn.execute(stmt)
	rows =  result.fetchall()
	values = []
	ids = []
	for i in rows:
		values.append(i[0])
		ids.append(i[1])
	diction = {"values": values ,'ids' : ids}
	# diction = {"values":values}
	return json.dumps(diction)
@app.route("/bldg")
def bldg():
	dist = request.args.get('dist')
	hi = request.args.get('hi')
	stmt = "select fld_Bldg_NM,fld_Bldg_SID from DataTable where fld_HI_SID = '" + hi + "' and fld_Dist_NM = '"+dist+"';"
	print(stmt)
	result = conn.execute(stmt)
	rows =  result.fetchall()
	values = []
	ids = []
	if rows == []:
		diction = {"values":None}
	else:
		for i in rows:
			print(i)
			values.append(i[0])
			ids.append(i[1])
		diction = { "values":values ,"ids" : ids}
	
	return json.dumps(diction)
		
@app.route("/data")
def hello():
    querystr = request.args.get('bldgid')
    stmt = "select * from DataTable where fld_Bldg_SID = '" + querystr + "';"
    print(stmt)
    result = conn.execute(stmt)
    rows =  result.fetchall()
    print(rows);
    null = False
    if (rows == []):
    	null = True
    fields = ["fld_Bldg_SID","fld_Bldg_DsgnStd","fld_Bldg_ID","fld_Bldg_UID","fld_Bldg_NM","fld_Bldg_HSFU","fld_Bldg_Oshp","fld_Bldg_YOC","fld_Bldg_GC","fld_Bldg_Typ","fld_Bldg_Use","fld_HI_ID","fld_HI_SID","fld_Bldg_FlrAr","fld_Bldg_Img0","fld_Bldg_Img1","fld_Bldg_Img2","fld_Bldg_Img3","fld_Bldg_Img4","fld_Bldg_Drw","fld_HI_Typ","fld_HI_Name","is_tallied","fld_Dist_NM","fld_Dist_ID","fld_Bldg","fld_Bldg_WPit","fld_Bldg_Plac","fld_Bldg_Inci"]
    j = 0
    return_dict = {}
    for i in fields:
    	if null:
    		return_dict[i] = ""
    	else:
    		return_dict[i] = rows[0][j]
    	# print(i)
    	j = j + 1

    return json.dumps(return_dict)

@app.route("/send", methods=['GET', 'POST'])
def send():
	# handles post requests
	# for i in request.files():
		# print(request.files[i]);
	
	if request.form:
		print("processing request now")
		sid = process_request(request.form)
		if not(sid == 0):
			aid = str(sid)
		else:
			aid = request.form['fld_Bldg_SID']
		if request.files:
			print("processing files")
			process_files(request.files,aid)
	return "Done"

def process_request(form_data):
	print(form_data)
	print(form_data['fld_Bldg_SID'])
	total = 0
	new = 0
	id_new = form_data['fld_HI_SID']
	if not(form_data['fld_Bldg_SID']):	
		new = 1
		query = "SELECT count(*) FROM `DataTable` WHERE `is_new` = '1' or `is_new` = '2'"
		result = conn.execute(query)
		for i in result:
			total = i[0]
		total = total + 99999000
		total1 = total
	else:
		total1 = form_data['fld_Bldg_SID']
	if (form_data['hi_new'] == '1'):
		new = 2
		query = "SELECT count(*) FROM `DataTable` WHERE `is_new` = '2'"
		result = conn.execute(query)
		for i in result:
			new_id = i[0]
		id_new = str(888880000 + new_id)

	query = "INSERT INTO DataTable VALUES ('"+ str(total1)+"', '"+ form_data['fld_Bldg_DsgnStd']+"', '"+ form_data['fld_Bldg_ID']+"', '"+ form_data['fld_Bldg_UID']+"', '"+ form_data['fld_Bldg_NM']+"', '"+form_data['fld_Bldg_HSFU']+"', '"+ form_data['fld_Bldg_Oshp']+"', '"+form_data['fld_Bldg_YOC']+"', '"+form_data['fld_Bldg_GC']+"', '"+form_data['fld_Bldg_Typ']+"', '"+form_data['fld_Bldg_Use']+"', '"+form_data['fld_HI_ID']+"', '"+id_new+"', '"+form_data['fld_Bldg_FlrAr']+"', '"+ form_data['fld_Bldg_Img0']+"', '"+form_data['fld_Bldg_Img1']+"','"+form_data['fld_Bldg_Img2']+"', '"+form_data['fld_Bldg_Img3']+"', '"+form_data['fld_Bldg_Img4']+"', '"+form_data['fld_Bldg_Drw']+"', '"+form_data['fld_HI_Typ']+"', '"+form_data['fld_HI_Name']+"', '1' , '"+form_data['fld_Dist_NM']+"', '"+form_data['fld_Dist_ID']+"',"+str(new)+",'"+form_data['fld_Bldg_WPit']+"','"+form_data['fld_Bldg_Plac']+"','"+form_data['fld_Bldg_Inci']+"') ON DUPLICATE KEY "+"UPDATE fld_Bldg_SID='"+ form_data['fld_Bldg_SID']+"', fld_Bldg_DsgnStd ='"+ form_data['fld_Bldg_DsgnStd']+"', fld_Bldg_ID  ='"+ form_data['fld_Bldg_ID']+"', fld_Bldg_UID  ='"+ form_data['fld_Bldg_UID']+"', fld_Bldg_NM  ='"+ form_data['fld_Bldg_NM']+"', fld_Bldg_HSFU ='"+form_data['fld_Bldg_HSFU']+"', fld_Bldg_Oshp ='"+ form_data['fld_Bldg_Oshp']+"', fld_Bldg_YOC ='"+form_data['fld_Bldg_YOC']+"', fld_Bldg_GC ='"+form_data['fld_Bldg_GC']+"', fld_Bldg_Typ ='"+form_data['fld_Bldg_Typ']+"', fld_Bldg_Use ='"+form_data['fld_Bldg_Use']+"', fld_HI_ID ='"+form_data['fld_HI_ID']+"', fld_HI_SID ='"+form_data['fld_HI_SID']+"', fld_Bldg_FlrAr ='"+form_data['fld_Bldg_FlrAr']+"', fld_Bldg_Img0  ='"+ form_data['fld_Bldg_Img0']+"', fld_Bldg_Img1 ='"+form_data['fld_Bldg_Img1']+"', fld_Bldg_Img2 ='"+form_data['fld_Bldg_Img2']+"', fld_Bldg_Img3 ='"+form_data['fld_Bldg_Img3']+"', fld_Bldg_Img4 ='"+form_data['fld_Bldg_Img4']+"', fld_Bldg_Drw ='"+form_data['fld_Bldg_Drw']+"', fld_HI_Typ ='"+form_data['fld_HI_Typ']+"', fld_HI_Name ='"+form_data['fld_HI_Name']+"',fld_Dist_NM='"+form_data['fld_Dist_NM']+"', fld_Dist_ID ='"+form_data['fld_Dist_ID']+"', is_tallied  = '1' ,fld_Bldg_WPit = '"+form_data['fld_Bldg_WPit']+"',fld_Bldg_Inci = '"+form_data['fld_Bldg_Inci']+"',fld_Bldg_Plac = '"+form_data['fld_Bldg_Plac']+"';"
	# print(query1)
	# query = "UPDATE fld_Bldg_SID='"+ form_data['fld_Bldg_SID']+"', fld_Bldg_DsgnStd ='"+ form_data['fld_Bldg_DsgnStd']+"', fld_Bldg_ID  ='"+ form_data['fld_Bldg_ID']+"', fld_Bldg_UID  ='"+ form_data['fld_Bldg_UID']+"', fld_Bldg_NM  ='"+ form_data['fld_Bldg_NM']+"', fld_Bldg_HSFU ='"+form_data['fld_Bldg_HSFU']+"', fld_Bldg_Oshp ='"+ form_data['fld_Bldg_Oshp']+"', fld_Bldg_YOC ='"+form_data['fld_Bldg_YOC']+"', fld_Bldg_GC ='"+form_data['fld_Bldg_GC']+"', fld_Bldg_Typ ='"+form_data['fld_Bldg_Typ']+"', fld_Bldg_Use ='"+form_data['fld_Bldg_Use']+"', fld_HI_ID ='"+form_data['fld_HI_ID']+"', fld_HI_SID ='"+form_data['fld_HI_SID']+"', fld_Bldg_FlrAr ='"+form_data['fld_Bldg_FlrAr']+"', fld_Bldg_Img0  ='"+ form_data['fld_Bldg_Img0']+"', fld_Bldg_Img1 ='"+form_data['fld_Bldg_Img1']+"', fld_Bldg_Img2 ='"+form_data['fld_Bldg_Img2']+"', fld_Bldg_Img3 ='"+form_data['fld_Bldg_Img3']+"', fld_Bldg_Img4 ='"+form_data['fld_Bldg_Img4']+"', fld_Bldg_Drw ='"+form_data['fld_Bldg_Drw']+"', fld_HI_Typ ='"+form_data['fld_HI_Typ']+"', fld_HI_Name ='"+form_data['fld_HI_Name']+"',fld_Dist_NM='"+form_data['fld_Dist_NM']+"', fld_Dist_ID ='"+form_data['fld_Dist_ID']+"', is_tallied  = '1' ;"
	# query = "UPDATE DataTable SET fld_Bldg_SID='"+ form_data['fld_Bldg_SID']+"', fld_Bldg_DsgnStd ='"+ form_data['fld_Bldg_DsgnStd']+"', fld_Bldg_ID  ='"+ form_data['fld_Bldg_ID']+"', fld_Bldg_UID  ='"+ form_data['fld_Bldg_UID']+"', fld_Bldg_NM  ='"+ form_data['fld_Bldg_NM']+"', fld_Bldg_HSFU ='"+form_data['fld_Bldg_HSFU']+"', fld_Bldg_Oshp ='"+ form_data['fld_Bldg_Oshp']+"', fld_Bldg_YOC ='"+form_data['fld_Bldg_YOC']+"', fld_Bldg_GC ='"+form_data['fld_Bldg_GC']+"', fld_Bldg_Typ ='"+form_data['fld_Bldg_Typ']+"', fld_Bldg_Use ='"+form_data['fld_Bldg_Use']+"', fld_HI_ID ='"+form_data['fld_HI_ID']+"', fld_HI_SID ='"+form_data['fld_HI_SID']+"', fld_Bldg_FlrAr ='"+form_data['fld_Bldg_FlrAr']+"', fld_Bldg_Img0  ='"+ form_data['fld_Bldg_Img0']+"', fld_Bldg_Img1 ='"+form_data['fld_Bldg_Img1']+"', fld_Bldg_Img2 ='"+form_data['fld_Bldg_Img2']+"', fld_Bldg_Img3 ='"+form_data['fld_Bldg_Img3']+"', fld_Bldg_Img4 ='"+form_data['fld_Bldg_Img4']+"', fld_Bldg_Drw ='"+form_data['fld_Bldg_Drw']+"', fld_HI_Typ ='"+form_data['fld_HI_Typ']+"', fld_HI_Name ='"+form_data['fld_HI_Name']+"',fld_Dist_NM='"+form_data['fld_Dist_NM']+"', fld_Dist_ID ='"+form_data['fld_Dist_ID']+"', is_tallied  = '1' WHERE fld_Bldg_SID ='"+form_data['fld_Bldg_SID']+"';"
	
	print(query)
	result = conn.execute(query)
	return total
def process_files(file_data,name):
	j = 0
	for i in file_data:
		
		file_data[i].save('./images/'+name+"_"+str(j)+'.'+file_data[i].filename.split('.')[len(file_data[i].filename.split('.'))-1])
		j = j+1
if __name__ == "__main__":
    # app.run(host='192.168.100.14', port=8888)
    app.run(host='192.168.17.108', port=8888)
    # app.run(host='192.168.100.8', port=8888)
    # app.run(host='127.0.0.1', port=8888)



