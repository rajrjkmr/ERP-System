import os
import datetime
import pandas as pd
import numpy
from pandas import ExcelWriter
from pandas import ExcelFile
import MySQLdb
import sys
import random
con=MySQLdb.connect("localhost","root","root","ifet")
cursor=con.cursor()
from flask import Flask,request,render_template,session,redirect,jsonify,send_from_directory
from werkzeug import secure_filename
# from database import insert,select,update,delete
now = datetime.datetime.now().strftime('%d-%m-%Y')
now1 = datetime.datetime.now()
app=Flask(__name__)
app.secret_key = "tam"
app.config['UPLOAD_FOLDER'] = 'static/img/upload'
#LOGIN SESSION
@app.route("/")
def login():
	return render_template("login.html")
@app.route("/login_validate",methods=['POST'])
def login_validate():
	data= request.get_json()
	user_id=data.get("user_name")
	password=data.get("password")
	cursor.execute("SELECT *FROM test WHERE Mobile='%s' AND Mobile='%s'" %(user_id,password))
	data=cursor.fetchone()
	if data==None:
		re="n"	
	else:
		session['user_id']=user_id
		re="s"
	return re
@app.route("/dashboard")
def dashboard():
	user_id=session['user_id']
	return render_template("dashboard_new.html",user_id=user_id)
@app.route("/user.json")
def user_json():
	user_id=session['user_id']
	session['user_id']=user_id
	session_manage(user_id)
	# user_id="9442101456"
	# name="MATILDA S"
	# user_id="9677354556"	
	# name="NIVETHA KUMARI"
	# batch="2014"
	# access="STAFF"
	# dept="IT"
	# sec="A"

	# print user_id
	cursor.execute("SELECT *FROM test WHERE Mobile = '%s'"%(user_id))
	x=cursor.fetchone()
	des=[]
	# print x,
	for y in cursor.description:
	  des.append(y[0])
	  
	
	data={des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8],des[9]:x[9],des[10]:x[10],des[11]:x[11],des[12]:x[12],des[13]:x[13],des[14]:x[14],des[15]:x[15],des[16]:x[16],des[17]:x[17],des[18]:x[18],des[19]:x[19],des[20]:x[20],des[21]:x[21],des[22]:x[22],des[23]:x[23],des[24]:x[24],des[25]:x[25],des[26]:x[26],des[27]:x[27],des[28]:x[28],des[29]:x[29],des[30]:x[30],des[31]:x[31],des[32]:x[32],des[33]:x[33],des[34]:x[34],des[35]:x[35],des[36]:x[36],des[37]:x[37],des[38]:x[38],des[39]:x[39],des[40]:x[40],des[41]:x[41],des[42]:x[42],des[43]:x[43],des[44]:x[44],des[45]:x[45],des[46]:x[46],des[47]:x[47]}
	return jsonify(data)
def session_manage(user_id):
	cursor.execute("SELECT * FROM test WHERE Mobile = '%s'"%(user_id))
	x=cursor.fetchone()
	session["name"]=x[1]
	session["batch"]=x[45]
	session["access"]=x[44]
	session["dept"]=x[14]
	session["sec"]=x[46]
@app.route("/user_update.json",methods=['POST'])
def user_update():
	data=request.get_json()
	for x in data:
		 
		sql="UPDATE test SET `"+x+"`='%s'WHERE Mobile='%s'" %(data[x],data['Mobile'])
		cursor.execute(sql)
		con.commit()

	return "success"		
 
@app.route("/add_subject")
def add_subject():
	return render_template("add_subject.html")
@app.route("/subject.json")
def subjectjson():
	cursor.execute("SELECT *FROM subject")
	data=cursor.fetchall()
	datas=[]
	for x in data:
		datas.append({"subject_code":x[0],"subject_name":x[1],"sem":x[2],"id":x[3],"dept":x[4]})
	return jsonify(datas)
@app.route("/subject_delete/<id>")
def subject_delete(id):
	v_id=id
	cursor.execute("DELETE FROM subject WHERE id='%s'" %(id))
	con.commit()
	return "success"
@app.route("/add_new_subject",methods=["POST"])
def add_new_subject():
	data=request.get_json()
	subject_code=data.get("subject_code")
	subject_name=data.get("subject_name")
	sem=data.get("sem")
	dept=session['dept']
	cursor.execute("INSERT INTO subject(`subject_code`,`subject_name`,`sem`,`dept`) VALUES('%s','%s','%s','%s')" %(subject_code,subject_name,sem,dept))
	con.commit()
	return "Add sucessfully"
@app.route("/update_subject",methods=["POST"])
def update_subject():
  # var va={"id":id,"subject_code":subject_code,"subject_name":subject_name,"sem":sem};
	data=request.get_json()
	id=data.get("id")
	subject_code=data.get("subject_code")
	subject_name=data.get("subject_name")
	sem=data.get("sem")
	cursor.execute("UPDATE subject SET subject_code='%s',subject_name='%s',sem='%s' WHERE id='%s'" %(subject_code,subject_name,sem,id))
	con.commit()

	return "sucess to update"
#subject Handeker 
@app.route("/subject_handler")
def subject_handler():
	cursor.execute("SELECT *FROM subject")
	subject=cursor.fetchall()
	cursor.execute("SELECT *FROM test")
	staff=cursor.fetchall()
	batch=["2014-2018","2015-2019","2016-2020","2017-2021"]


	return render_template("subject_handler.html",subject=subject,staff=staff,batch=batch)
@app.route("/subject_handler_json")
def subject_handler_json():
	cursor.execute("SELECT *FROM subject_handler")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7]})
	
	return jsonify(i)
@app.route("/subject_handler_delete/<id>")
def subject_handler_delete(id):
	v_id=id
	cursor.execute("DELETE FROM subject_handler WHERE id='%s'" %(id))
	con.commit()
	return "success"

#TIME TABLE
@app.route("/timetable.json")
def jsontime():
	id=session['user_id']	
	name=session['name']
	batch=session['batch']
	access=session['access']
	dept=session['dept']
	section=session['sec']
	id=batch+dept+section+str(id)
	cursor.execute("SELECT * FROM timetable WHERE id='%s'" %(id))
	de=[]
	dd=[]
	for d in cursor.description:
		de.append(d[0])
	for x in cursor.fetchall():
		dd.append({de[0]:x[0], de[1]:x[1], de[2]:x[2], de[3]:x[3], de[4]:x[4], de[5]:x[5], de[6]:x[6], de[7]:x[7], de[8]:x[8], de[9]:x[9], de[10]:x[10], de[11]:x[11], de[12]:x[12], de[13]:x[13], de[14]:x[14], de[15]:x[15], de[16]:x[16], de[17]:x[17], de[18]:x[18], de[19]:x[19], de[20]:x[20], de[21]:x[21], de[22]:x[22], de[23]:x[23], de[24]:x[24], de[25]:x[25], de[26]:x[26], de[27]:x[27], de[28]:x[28], de[29]:x[29], de[30]:x[30], de[31]:x[31], de[32]:x[32], de[33]:x[33], de[34]:x[34], de[35]:x[35], de[36]:x[36], de[37]:x[37], de[38]:x[38], de[39]:x[39], de[40]:x[40], de[41]:x[41], de[42]:x[42], de[43]:x[43], de[44]:x[44], de[45]:x[45], de[46]:x[46], de[47]:x[47], de[48]:x[48], de[49]:x[49], de[50]:x[50], de[51]:x[51]})
	return jsonify(dd)
@app.route("/timetableadd",methods=["POST"])
def timetableadd():
	data=request.get_json()
	print data
	return data

	
@app.route("/timetable")
def sem_sub():
	# sem=sem_pick(int(session["batch"]))
#	print sem
	# section=session['sec']
	# dept=session['dept']
	# name=session["name"]
#	print dept
#	sub=subj
	# access=session['access']
	# id=session['user_id']
	# batch=session['batch']
	id=session['user_id']	
	name=session['name']
	batch=session['batch']
	access=session['access']
	dept=session['dept']
	section=session['sec']
	sem=sem_pick(int(batch))
	id=batch+dept+section+str(id)
	cursor.execute("SELECT *FROM `subject_handler` WHERE subject_handler ='%s'"%(name))
	sub=[]
	for x in cursor.fetchone():
		sub.append(x)
	cursor.execute("SELECT *from subject WHERE sem='%s' AND dept='%s'" %(sem,dept))
	subject=cursor.fetchall()
	cursor.execute("SELECT *from timetable WHERE id='%s'" %(id))
	val1=cursor.fetchall()
#   	print sub[1]
  	return render_template("add_timetable.html",subjects=subject,val1=val1,dept=dept,sem=sem,sub=sub[1])

@app.route("/delete_timetable")
def delete_timetable():
	batch=session['batch']
	sem=sem_pick(int(batch))
	section=session['sec']
	dept=session['dept']
	access=session['access']
	dept=session['dept']
	delete.delete_timetable(dept,sem,section)
	return redirect("/timetable")
@app.route("/add_new_timetable",methods=['POST'])
def add_new_timetable():
	data=request.get_json()
	print session['user_id']
	id=session['user_id']
	sec=session['sec']
	batch=session['batch']
	dept=session['dept']
	id=batch+dept+sec+str(id)
	period11=data.get("period11")
	period12=data.get("period12")
	period13=data.get("period13")
	period14=data.get("period14")
	period15=data.get("period15")
	period16=data.get("period16")
	period17=data.get("period17")
	period18=data.get("period18")
	period21=data.get("period21")
	period22=data.get("period22")
	period23=data.get("period23")
	period24=data.get("period24")
	period25=data.get("period25")
	period26=data.get("period26")
	period27=data.get("period27")
	period28=data.get("period28")
	period31=data.get("period31")
	period32=data.get("period32")
	period33=data.get("period33")
	period34=data.get("period34")
	period35=data.get("period35")
	period36=data.get("period36")
	period37=data.get("period37")
	period38=data.get("period38")
	period41=data.get("period41")
	period42=data.get("period42")
	period43=data.get("period43")
	period44=data.get("period44")
	period45=data.get("period45")
	period46=data.get("period46")
	period47=data.get("period47")
	period48=data.get("period48")
	period51=data.get("period51")
	period52=data.get("period52")
	period53=data.get("period53")
	period54=data.get("period54")
	period55=data.get("period55")
	period56=data.get("period56")
	period57=data.get("period57")
	period58=data.get("period58")
	period61=data.get("period61")
	period62=data.get("period62")
	period63=data.get("period63")
	period64=data.get("period64")
	period65=data.get("period65")
	period66=data.get("period66")
	period67=data.get("period67")
	period68=data.get("period68")
	cursor.execute("INSERT INTO timetable(`id`,	`dept`,`batch`,`sec`,`period11`, `period12`, `period13`, `period14`, `period15`, `period16`, `period17`, `period18`, `period21`, `period22`, `period23`, `period24`, `period25`, `period26`, `period27`, `period28`, `period31`, `period32`, `period33`, `period34`, `period35`, `period36`, `period37`, `period38`, `period41`, `period42`, `period43`, `period44`, `period45`, `period46`, `period47`, `period48`, `period51`, `period52`, `period53`, `period54`, `period55`, `period56`, `period57`, `period58`, `period61`, `period62`, `period63`, `period64`, `period65`, `period66`, `period67`, `period68`) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(id,dept,batch,sec,period11, period12, period13, period14, period15, period16, period17, period18, period21, period22, period23, period24, period25, period26, period27, period28, period31, period32, period33, period34, period35, period36, period37, period38, period41, period42, period43, period44, period45, period46, period47, period48, period51, period52, period53, period54, period55, period56, period57, period58, period61, period62, period63, period64, period65, period66, period67, period68))
	con.commit()
	return "success"


@app.route("/add_new_subject_handler",methods=["POST"])
def add_new_subject_handler():
	data=request.get_json()
	staff_name=data.get("staff_name")
	subject=data.get("subject")
	batch=data.get("batch")
	sec=data.get("sec")
	sem=sem_pick(int(batch[0:4]))
	dept=session['dept']
	cursor.execute("INSERT INTO subject_handler(`subject_name`, `subject_handler`, `sem`, `dept`, `date`, `sec`, `batch`) VALUES('%s','%s','%s','%s',now(),'%s','%s')" %(subject,staff_name,sem,dept,sec,batch))
	con.commit()
	return "sucess"
#BULK UPLOAD
@app.route("/bulk_data")
def bulk_data():
	return render_template("bulk_upload.html")
@app.route("/bulk_upload",methods=['POST','GET'])
def bulk_upload():
	files=request.files['file']
	file_type=request.form['selectbasic']
	filename = secure_filename(files.filename)
	filename.replace(' ','-')
	files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	if file_type=="staff":
		staff_bulck_upload(filename)
		
	else:
		pass


	return redirect("/bulk_data")
	
	
def staff_bulck_upload(*filename):
	con=MySQLdb.connect("localhost","root","tam","ifet")
	obj=con.cursor() 
	df = pd.read_excel("static/img/upload/"+filename[0], sheetname='Sheet1')
	ch=[u'Aicte_id', u'Left_hand', u'Name', u'Gender', u'FatherName', u'Add1', u'MotherName', u'Add2', u'City_Village', u'Postal', u'Religion', u'State', u'Caste', u'DoB', u'PAN', u'LandLine', u'STD', u'Email', u'Mobile', u'staff_des', u'Course', u'DA', u'Facultytype', u'Doj', u'Gross', u'Basic', u'phd', u'PG', u'PGyear', u'UG', u'pgins', u'pguni', u'pgper', u'ugins', u'uguni', u'ugper', u'PGcourse', u'UGyear', u'UGCourse', u'Teachingexp', u'Bankno', u'Bankbranch', u'BankName', u'IFSC', u'photo_location', u'degree', u'college_id']
	ll=[]
	l=[]
	d=[]

	for x in  df.columns:
	  if x in ch:

	    l.append(x)
	  else:
	    del df[x]
	    d.append(x)
	values = df.values
	for x in values:
	  ll.append(x)



	table_name = "staff"
	e="'%s',"*len(l)
	e=e[0:len(e)-1]
	y=" VALUES("+e+")"
	for x in ll:
	  q=tuple(x)
	  # print q[18],q[18],q[2],q[19],q[20]
	  ta="INSERT INTO "  + table_name + " (" + ", ".join(l) + ")" +y %(q)
	  obj.execute(ta)
	  con.commit()
	  try:
	  	
	  	obj.execute("INSERT INTO login(`user_id`,`password`) VALUES('%s','%s')" %(q[18],q[18]) )
	  	con.commit()
	    # con.commit()
	  except Exception as e:
	  	
	    if e[0]==1062:

	      obj.execute("INSERT INTO  login(`user_id`, `password`) VALUES('%s','%s') ON DUPLICATE KEY UPDATE user_id='%s', password='%s'" %(q[18],q[18],q[18],q[18]) )
	      con.commit()


def student_bulck_upload(*filename):
	con=MySQLdb.connect("localhost","root","tam","ifet")
	obj=con.cursor() 
	df = pd.read_excel("static/img/upload/"+filename[0], sheetname='Sheet1')
	# ch=[u'Aicte_id', u'Left_hand', u'Name', u'Gender', u'FatherName', u'Add1', u'MotherName', u'Add2', u'City_Village', u'Postal', u'Religion', u'State', u'Caste', u'DoB', u'PAN', u'LandLine', u'STD', u'Email', u'Mobile', u'staff_des', u'Course', u'DA', u'Facultytype', u'Doj', u'Gross', u'Basic', u'phd', u'PG', u'PGyear', u'UG', u'pgins', u'pguni', u'pgper', u'ugins', u'uguni', u'ugper', u'PGcourse', u'UGyear', u'UGCourse', u'Teachingexp', u'Bankno', u'Bankbranch', u'BankName', u'IFSC', u'photo_location', u'degree', u'college_id']
	ll=[]
	l=[]
	d=[]

	for x in  df.columns:
	  if x in ch:

	    l.append(x)
	  else:
	    del df[x]
	    d.append(x)
	values = df.values
	for x in values:
	  ll.append(x)



	table_name = "staff"
	e="'%s',"*len(l)
	e=e[0:len(e)-1]
	y=" VALUES("+e+")"
	for x in ll:
	  q=tuple(x)
	  # print q[18],q[18],q[2],q[19],q[20]
	  ta="INSERT INTO "  + table_name + " (" + ", ".join(l) + ")" +y %(q)
	  obj.execute(ta)
	  con.commit()
	  try:
	  	
	  	obj.execute("INSERT INTO login(`user_id`,`password`) VALUES('%s','%s')" %(q[18],q[18]) )
	  	con.commit()
	    # con.commit()
	  except Exception as e:
	  	
	    if e[0]==1062:

	      obj.execute("INSERT INTO  login(`user_id`, `password`) VALUES('%s','%s') ON DUPLICATE KEY UPDATE user_id='%s', password='%s'" %(q[18],q[18],q[18],q[18]) )
	      con.commit()	
@app.route("/administrators")
def administrators():

	return render_template("administors.html")
@app.route("/hod")
def hod():

	return render_template("hod.html")
@app.route("/hod_view")
def hodv():
	return render_template("hodv.html")
@app.route("/letter_view.json")
def letter_view():
	cursor.execute("SELECT * FROM letter")
	des=[]
	d=cursor.fetchall() 
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	i.append({"len":len(d)})	
	for x in d:
	  i.append({des[1]:x[1],des[2]:x[2],des[3]:x[3]})	
	print i
	return jsonify(i)

@app.route("/uploads")
def uploads():
	return render_template("uploads.html")

@app.route("/attend")
def attend():
	# name="PAJANY M"

	# section="B"
	# dept="CSE"
	# access="FA"
	# id="9486520800"
	# batch="2016"
	id=session['user_id']	
	name=session['name']
	batch=session['batch']
	access=session['access']
	dept=session['dept']
	section=session['sec']
	sem=sem_pick(int(batch))
	day1=0
	day2=0
	day3=0
	day4=0
	day5=0
	day6=0
	cursor.execute("SELECT day FROM `attendence`")	
	for x in cursor.fetchall():
		if x[0]=='1':
			day1=x[0]
		elif x[0]=='2':
			day2=x[0]
		elif x[0]=='3':
			day3=x[0]
		elif x[0]=='4':
			day4=x[0]
		elif x[0]=='5':
			day5=x[0]
		else:
			day6=x[0]
	# print day1,day2,day3,day4,day5,day6		
	cursor.execute("SELECT *FROM stu ORDER BY Name ASC")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	testi=[]
	for x in cursor.fetchall():	  
		testi.append(list(x))
	des.append(testi)	
	return render_template("attend_attendence.html",data=testi,sem=sem,dept=dept,day1=day1,day2=day2,day3=day3,day4=day4,day5=day5,day6=day6)
@app.route("/tests")
def tests():
	# name=session["name"]
	# batch=session['batch']
	# dept=session['dept']
	# sem=sem_pick(int(batch))
	# name="PAJANY M"

	# section="B"
	# dept="CSE"
	# access="FA"
	# id="9486520800"
	# batch="2016"
	id=session['user_id']	
	name=session['name']
	batch=session['batch']
	access=session['access']
	dept=session['dept']
	section=session['sec']
	sem=sem_pick(int(batch))
	cursor.execute("SELECT *FROM `subject_handler` WHERE subject_handler ='%s'"%(name))
	subject=[]
	for x in cursor.fetchone():
		subject.append(x)
			
	cursor.execute("SELECT *FROM stu ORDER BY Name ASC")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	testi=[]
	for x in cursor.fetchall():	  
		testi.append(list(x))
	des.append(testi)	
	return render_template("tests_tests.html",data=testi,dept=dept,sem=sem,subject=subject[1])
@app.route('/testview.json/<Id>')
def test_view_json(Id):
	cursor.execute("SELECT * FROM tests WHERE userid = '%s'"%(Id))
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[2]:x[2],des[6]:x[6],des[7]:x[7]})		
	return jsonify(i)	
@app.route("/testsadd",methods=['POST'])
def testsadd():	
	data=request.form.to_dict()
	testtype=request.form['testtype']	
	
	# # testtype=request.form['testtype']
	# batch=session['']
	# dept=session['']
	# sem=sem_pick(batch)
	# # subjectcode=session['']
	# subject=session['']
	batch=session['batch']
	dept=session['dept']
	sem=sem_pick(int(batch))
	subject="SNA"
	for x in data:
		# print data[x]	
	
		cursor.execute("INSERT INTO test ( `userid`, `testtype`, `batch`, `dept`, `sem`, `subject`, `marks`) VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(x,testtype,batch,dept,sem,subject,data[x]))
		cursor.execute("DELETE FROM test WHERE userid = 'testtype' ")
		
		con.commit()
	# print data
	return str(data)

@app.route('/countries.json')
def jsonFile():
	cursor.execute("SELECT *FROM staff")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8],des[9]:x[9],des[10]:x[10],des[11]:x[11],des[12]:x[12],des[13]:x[13],des[14]:x[14],des[15]:x[15],des[16]:x[16],des[17]:x[17],des[18]:x[18],des[19]:x[19],des[20]:x[20],des[21]:x[21],des[22]:x[22],des[23]:x[23],des[24]:x[24],des[25]:x[25],des[26]:x[26],des[27]:x[27],des[28]:x[28],des[29]:x[29],des[30]:x[30],des[31]:x[31],des[32]:x[32],des[33]:x[33],des[34]:x[34],des[35]:x[35],des[36]:x[36],des[37]:x[37],des[38]:x[38],des[39]:x[39],des[40]:x[40],des[41]:x[41],des[42]:x[42],des[43]:x[43],des[44]:x[44],des[45]:x[45],des[46]:x[46],des[47]:x[47]})
	return jsonify(i)
@app.route('/student.json')
def studentjson():
	cursor.execute("SELECT * FROM stu ORDER BY Name ASC")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  # i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8],des[9]:x[9],des[10]:x[10],des[11]:x[11],des[12]:x[12],des[13]:x[13],des[14]:x[14],des[15]:x[15],des[16]:x[16],des[17]:x[17],des[18]:x[18],des[19]:x[19],des[20]:x[20],des[21]:x[21],des[22]:x[22],des[23]:x[23],des[24]:x[24],des[25]:x[25],des[26]:x[26],des[27]:x[27],des[28]:x[28],des[29]:x[29]})
		i.append(list(x))
	# return jsonify(i)
	des.append(i)
	return "hh"
@app.route('/student_view.json')
def student_view_json():
	cursor.execute("SELECT * FROM stu ORDER BY Name ASC")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8],des[9]:x[9],des[10]:x[10],des[11]:x[11],des[12]:x[12],des[13]:x[13],des[14]:x[14],des[15]:x[15],des[16]:x[16],des[17]:x[17],des[18]:x[18],des[19]:x[19],des[20]:x[20],des[21]:x[21],des[22]:x[22],des[23]:x[23],des[24]:x[24],des[25]:x[25],des[26]:x[26],des[27]:x[27],des[28]:x[28],des[29]:x[29]})
		
	return jsonify(i)	
@app.route('/viewattedence.json/<Id>')
def viewattedence(Id):
	cursor.execute("SELECT * FROM attendence WHERE id='%s'"%(Id))
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8]})
	return jsonify(i)

@app.route('/attendence_view.json')
def attendence_view():
	cursor.execute("SELECT * FROM attendence")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8]})
	return jsonify(i)	

@app.route('/tests_view.json')
def tests_view():
	cursor.execute("SELECT * FROM tests")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7]})	
	return jsonify(i)
	
@app.route('/viewuniversity.json/<Id>')
def viewuniversity(Id):
	cursor.execute("SELECT * FROM university WHERE id='%s'"%(Id))
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7]})
	return jsonify(i)


@app.route("/adduniv",methods=["POST"])
def adduniv():
	data=request.get_json()
	ids=data.get("id")
	dept=data.get("dept")
	batch=data.get("batch")
	sem=data.get("sem")
	sec=data.get("sec")
	p1=data.get("scode")
	p2=data.get("sub")
	p3=data.get("grade")	
	cursor.execute("INSERT INTO university (`id`,`batch`,`dept`,`sem`,`sec`,`scode`,`subject`,`grade`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(ids,batch,dept,sem,sec,p1,p2,p3))
	con.commit()
	return "Record Inserted successfully"
@app.route("/addattend",methods=["POST"])
def addattend():
	data=request.get_json()
	day=data.get("day")
	ids=data.get("id")
	dept=data.get("dept")
	batch=data.get("batch")
	sem=data.get("sem")
	sec=data.get("sec")
	# date=now
	p1=data.get("p1")
	p2=data.get("p2")
	p3=data.get("p3")
	p4=data.get("p4")
	p5=data.get("p5")
	p6=data.get("p6")
	p7=data.get("p7")
	p8=data.get("p8")
	# cursor.execute("INSERT INTO attendence (`day`,`date`,`id`,`dept`,`batch`,`sem`,`sec`,`p1`,`p2`,`p3`,`p4`,`p5`,`p6`,`p7`,`p8`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(day,date,ids,dept,batch,sem,sec,p1,p2,p3,p4,p5,p6,p7,p8))
	cursor.execute("INSERT INTO attendence (`day`,`date`,`id`,`dept`,`batch`,`sem`,`sec`,`period`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(day,now,ids,dept,batch,sem,sec,p1))
	con.commit()
	return "Record Inserted successfully"	
@app.route("/add_attend",methods=["POST"])
def add_attend():
	data=request.form.to_dict()
	cursor.execute("SELECT *FROM stu")
	p=cursor.fetchall()
	pp=[]
	pre=[]
	ab=[]
	temp=[]
	day=request.form['day']	
	dept="CSE"
	batch=2016
	sem=sem_pick(batch)
	sec="A"
	# print type(day)
	del data['day']
	for x in p:
		pp.append(x[29])
	for x in data:
		temp.append(int(x))
	for x in pp:
		if x in temp:
			ids=x		
			period="P"
			# print ids,period,day,dept,batch,sem,sec
			cursor.execute("INSERT INTO attendence (`day`,`date`,`id`,`dept`,`batch`,`sem`,`sec`,`period`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(day,now,ids,dept,batch,sem,sec,period))												
			con.commit()
		else:
			ids=x
			period="A"
			cursor.execute("INSERT INTO attendence (`day`,`date`,`id`,`dept`,`batch`,`sem`,`sec`,`period`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(day,now,ids,dept,batch,sem,sec,period))															
			con.commit()
		
		
	return redirect("/attend")
# @app.route("/staff")
# def staff():
# 	return render_template("staff.html")

def sem_pick(value):
	if now1.year-value==4:
		if now1.month>=6:
			sem=7
		else:
			sem=8
	elif now1.year-value==3:
		if now1.month<=6:
			sem=6
		else:
			sem=5
	elif now1.year-value==2:
		if now1.month<=6:
			sem=4
		else:
			sem=3
	else:
		if now1.month>=6:
			sem=1
		else:
			sem=2
	return sem
@app.route("/student")
def student():
	return render_template("student.html")		
	
@app.route("/staff")
def staff():
	return render_template("staff.html")
# @app.route("/staff_master_view")
# def staff_master_view():
# 	return render_template("staff_master_view.html")
@app.route("/access_update",methods=["POST"])
def access_update():
	data=request.get_json()
	Mobile=data.get("Mobile")
	access=data.get("access_type")
	batch=data.get("batch")
	sec=data.get("sec")
	cursor.execute("UPDATE test SET access='%s',batch = '%s', sec = '%s' WHERE Mobile='%s'" %(access,batch,sec,Mobile))
	con.commit()
	cursor.execute("UPDATE staff SET `access`='%s',`batch` = '%s', `sec` = '%s' WHERE Mobile='%s'" %(access,batch,sec,Mobile))	
	con.commit()
	# print Mobile,access,batch,sec	
	return "sucess to update"
@app.route("/staff.json")
def staffjson():
	cursor.execute("SELECT *FROM staff")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7],des[8]:x[8],des[9]:x[9],des[10]:x[10],des[11]:x[11],des[12]:x[12],des[13]:x[13],des[14]:x[14],des[15]:x[15],des[16]:x[16],des[17]:x[17],des[18]:x[18],des[19]:x[19],des[20]:x[20],des[21]:x[21],des[22]:x[22],des[23]:x[23],des[24]:x[24],des[25]:x[25],des[26]:x[26],des[27]:x[27],des[28]:x[28],des[29]:x[29],des[30]:x[30],des[31]:x[31],des[32]:x[32],des[33]:x[33],des[34]:x[34],des[35]:x[35],des[36]:x[36],des[37]:x[37],des[38]:x[38],des[39]:x[39],des[40]:x[40],des[41]:x[41],des[42]:x[42],des[43]:x[43],des[44]:x[44],des[45]:x[45],des[46]:x[46],des[47]:x[47],des[48]:x[48],des[49]:x[49]})

	return jsonify(i)	
# def te(f):
# 	filename = secure_filename(f.filename)
# 	files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 	file=filename
# 	print file

@app.route("/logout")
def logout():
	session.pop('user_name', None)
	session.pop('access',None)
	session.pop('dept',None)
	session.pop('user_id',None)
	return redirect("/")

if __name__=="__main__":
	# print dep()
	# app.run("192.168.137.41",88,debug=True)
	# app.run(debug=True)
	app.run(debug=True)
	# app.run("tamizh",88,debug=True)



	
