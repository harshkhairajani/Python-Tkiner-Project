#Required Libraries
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import socket
import requests
import bs4

#Bulid Database 
con = None
try:
	con = connect("test.db")  
	print ("connected")
	cursor = con.cursor()
	sql = "create table student(rno int primary key, name text, marks int)"
	cursor.execute(sql)    
	print("table created")
except OperationalError as e:
	print (":)")
except Exception as e1:
	showerror("Database Error")	
finally:
	if con is not None:
		con.close()         
		print("disconnected")		

#Show:add and hide:root
def f1():
	adst.deiconify()
	root.withdraw()
	entrno.delete(0,"end")
	entname.delete(0,"end")
	entmarks.delete(0,"end")

#Show:root and hide:add
def f2():
	root.deiconify()
	adst.withdraw()

#Show:root and hide:view
def f4():
	root.deiconify()
	vist.withdraw()

#Show:delete and hide:root
def f6():
	dlt.deiconify()
	root.withdraw()
	entrno3.delete(0,"end")

#Show:update and hide:root
def f7():
	upd.deiconify()
	root.withdraw()

#Show:root and hide:delete
def f8():
	root.deiconify()
	dlt.withdraw()

#Show:root and hide:update
def f9():
	root.deiconify()
	upd.withdraw()

#Show:pro and hide:update
def f10():
	pro.deiconify()
	upd.withdraw()  

#Show view and hide root, processing data to view from database 						
def f3():
	stdata.delete(1.0, END)
	vist.deiconify()
	root.withdraw()
	con = None
	try:
		con = connect("test.db")
		print("connected")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info  = info + "Roll No:" + str(d[0]) + " Name:" +str(d[1]) + " Marks:" + str(d[2]) + "\n"
		stdata.insert(INSERT, info)

	except Exception as e:
		print("Select Issue:", e)

	finally:
		if con is not None:
			con.close()
			print("Disconnected")			
			
#Save Button
def f5():
	con = None
	try:
		con = connect("test.db")
		rno = int(entrno.get())
		if rno<0:
			raise Exception(showerror("Error","Roll number cannot be negative!"))
			con.rollback()
		elif rno=="":
			raise Exception(showerror("Error","Roll number cannot be blank!"))
			con.rollback()		
		name = entname.get()
		if len(name)<2:
			raise Exception(showerror("Error","Name must be atleast two characters!"))
			con.rollback()
		elif name.isdigit():
			raise Exception (showerror("Error","Name cannot be numerical digits!"))
			con.rollback()
		elif name=="":
			raise Exception(showerror("Error","Name cannot be left blank!"))
	except ValueError:
		showerror("Error","Roll should be in integers!")
		con.rollback()			
	try:					 
		marks = int(entmarks.get())
		if marks>100:
			raise Exception (showerror("Error","Marks cannot be above 100!"))
			con.rollback()
		elif marks<0:
			raise Exception (showerror("Error","Marks cannot be below 0"))
			con.rollback()
		args = (rno, name, marks)
		cursor= con.cursor()
		sql = "insert into student values('%d', '%s', '%d')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success", "Record added!")
		entrno.delete(0,"end")
		entname.delete(0,"end")
		entmarks.delete(0,"end")	
	except ValueError:
		showerror("Error","Marks should be in integers!")
		con.rollback()
	except IntegrityError:
		showerror("Error","Roll number already registered!")				
	finally:
		if con is not None:
			con.close()
	

#Delete Button
def f11():
	con = None
	try:
		con = connect("test.db")
		rno3 = int(entrno3.get())
		if rno3<0:
			raise Exception(showerror("Error","Roll number cannot be negative!"))
			con.rollback()
		else:	
			arg = (rno3)
			cursor = con.cursor()
			sql = "delete from student where rno = '%d'"
			cursor.execute(sql % arg)
			if cursor.rowcount >= 1:
				con.commit()
				showinfo("Success", "Record deleted!")
				entrno3.delete(0,"end")
			else:
				showerror("Error","Record does not exists!")	
	except ValueError as e:
		showerror("Error","Roll number must be integers only!")
		con.rollback()

	finally:
		if con is not None:
			con.close()	

#Update name and marks
def f12():
	con = None
	try:
		con = connect("test.db")
		rno2 = int(entrno2.get())
		if rno2<0:
			raise Exception(showerror("Error","Roll number cannot be negative!"))
			con.rollback()
		elif rno2=="":
			raise Exception(showerror("Error","Roll number cannot be blank!"))
			con.rollback()		
		name2 = entname2.get()
		if len(name2)<2:
			raise Exception(showerror("Error","Name must be atleast two characters!"))
			con.rollback()
		elif name2.isdigit():
			raise Exception (showerror("Error","Name cannot be numerical digits!"))
			con.rollback()
		elif name2=="":
			raise Exception(showerror("Error","Name cannot be left blank!"))
	except ValueError:
		showerror("Error","Roll No. should be in integers!")
		con.rollback()		
	try:					 
		marks2 = int(entmarks2.get())
		if marks2>100:
			raise Exception (showerror("Error","Marks cannot be above 100!"))
			con.rollback()
		if marks2<0:
			raise Exception (showerror("Error","Marks cannot be below 100!"))
			con.rollback()
		args1 = (name2, marks2, rno2)
		cursor = con.cursor()
		sql = "update student set name = '%s', marks = '%d' where rno = '%d'"
		cursor.execute(sql % args1)
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("Success","Record Updated!")
			entrno2.delete(0,"end")
			entname2.delete(0,"end")
			entmarks2.delete(0,"end")
		else:
			showerror("Error","Record does not exists!")	
	except ValueError:
		showerror("Error","Marks should be integers!")
		con.rollback()
	finally:
		if con is not None:
			con.close()
#Graph
def f14():
	con = connect("test.db")
	cursor = con.cursor()
	data1 = pd.read_sql_query("select * from student order by marks DESC LIMIT 5", con)
	names = data1['name'].tolist()
	marksx = data1['marks'].tolist()
	plt.bar(names, marksx, color='g', width=0.5)
	plt.title("Toppers' Performance Graph")
	plt.xlabel("Names")
	plt.ylabel("Marks")
	plt.grid()
	plt.show()

#=========================
#main_window(root)
#=========================

root = Tk()
root.title("S.M.S")
root.geometry("920x560+400+100")
root.configure(background='Lightcyan')

btnAdd = Button(root, text="ADD", font=("verdana", 20, "bold"), width=10, command=f1)			
btnView = Button(root, text="VIEW", font=("verdana", 20, "bold"), width=10, command=f3)
btnUpdate = Button(root, text="UPDATE", font=("verdana", 20, "bold"), width=10, command=f7)
btnDelete = Button(root, text="DELETE", font=("verdana", 20, "bold"), width=10, command=f6)
btnGraph = Button(root, text="CHARTS", font=("verdana", 20, "bold"), width=10, command=f14)


#===========================================================================================================================================
#Print Location of user 
#=========================
 
try:
	res = requests.get("https://ipinfo.io/")
	data = res.json()
	city_name = data['city']
except OSError as e:
	print("issue ", e)

var_1 = StringVar()
var_1.set(city_name)
lbllocation = Label(root, textvariable= var_1, font=("verdana", 14, "bold"), width=10, anchor=NW)
lblloc = Label(root, text= "Location:", font=("verdana", 14, "bold"), width=10, anchor=NW)
lblloc.place(x=10, y=400)
lbllocation.place(x=10,y=440)

#=========================
#Print temperature
#=========================

try:
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name 
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address =  a1 + a2  + a3 		
	res = requests.get(api_address)
	data = res.json()
	main = data['main']
	temperature = main['temp']
except OSError as e:
	print("issue ", e)
var_2 = StringVar()
var_2.set(temperature)
lbltemperature = Label(root, textvariable= var_2, font=("verdana", 14, "bold"), width=10, anchor=NE)
lbltemp = Label(root, text= "Temperature:", font=("verdana", 14, "bold"), width=12, anchor=NE)
lbltemp.place(x=530 ,y=400)
lbltemperature.place(x=530 ,y=450)

#=========================
#Print QOTD
#=========================
'''
try:
	res1 = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res1.text, "html.parser")
	data = soup.find("img", {"class": "p-qotd"})
	mot = data['alt']
except Exception as e:
	print("issue", e)
main_3 = StringVar()
#main_3.set(mot)
lblqotd = Label(root, textvariable= main_3, font=("verdana", 14, "bold"))
lblquote = Label(root, text= "QOTD:", font=("verdana", 14, "bold"))
lblquote.place(x=10, y=490)
lblqotd.place(x=10,y=510)
'''
#===============================================================================================================================================


btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnGraph.pack(pady=10)

#=====================================================================================================
#add_window(adst)
#=========================


adst = Toplevel(root)
adst.title("Add Student")
adst.geometry("920x560+450+120")
adst.configure(background='Lightpink')
adst.withdraw()

lblrno = Label(adst, text="Enter Roll No.", font=("verdana", 20, "bold"))
entrno = Entry(adst, bd=5, font=("verdana", 20, "bold"))
lblname = Label(adst, text="Enter Name", font=("verdana", 20, "bold"))
entname = Entry(adst, bd=5, font=("verdana", 20, "bold"))
lblmarks = Label(adst, text="Enter Marks", font=("verdana", 20, "bold"))
entmarks = Entry(adst, bd=5, font=("verdana", 20, "bold"))
btnsave = Button(adst, text="Save", font=("verdana", 20, "bold"), command=f5)
btnback = Button(adst, text="Back", font=("verdana", 20, "bold"), command=f2)

lblrno.pack(pady=10)
entrno.pack(pady=10)
lblname.pack(pady=10)
entname.pack(pady=10)
lblmarks.pack(pady=10)
entmarks.pack(pady=10)
btnsave.pack(pady=15)
btnback.pack(pady=5)

#=====================================================================================================
#view_window(vist)
#=========================

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("920x560+400+100")
vist.configure(background="Lightblue")
vist.withdraw()

stdata = ScrolledText(vist, width=35,height=13, font=("Calibri", 20, "bold") ,bg="Lightpink")
btnvback = Button(vist, text="Back", font=("verdana", 20, "bold"), command=f4)

stdata.pack(pady=15)
btnvback.pack(pady=10)

#=====================================================================================================
#update_window(upd)
#=========================

upd = Toplevel()
upd.title("Update St.")
upd.geometry("920x560+400+100")
upd.configure(background='Lightyellow')
upd.withdraw()

lblrno2 = Label(upd, text="Enter Roll No. to change details", font=("verdana", 20, "bold"))
entrno2 = Entry(upd, bd=5, font=("verdana", 20, "bold"))
lblname2 = Label(upd, text="Enter Name", font=("verdana", 20, "bold"))
entname2 = Entry(upd, bd=5, font=("verdana", 20, "bold"))
lblmarks2 = Label(upd, text="Enter Marks", font=("verdana", 20, "bold"))
entmarks2 = Entry(upd, bd=5, font=("verdana", 20, "bold"))
btnupd = Button(upd, text="Update", font=("verdana", 20, "bold"), command=f12)
btnuback = Button(upd, text="Back", font=("verdana", 20, "bold"), command=f9)

lblrno2.pack(pady=10)
entrno2.pack(pady=10)
lblname2.pack(pady=10)
entname2.pack(pady=10)
lblmarks2.pack(pady=10)
entmarks2.pack(pady=10)
btnupd.pack(pady=10)
btnuback.pack(pady=10)

#=====================================================================================================
#delete_window
#=========================

dlt = Toplevel()
dlt.title("Delete St.")
dlt.geometry("920x560+400+100")
dlt.configure(background='Lightblue')
dlt.withdraw()

lblrno3 = Label(dlt, text="Enter Roll No. to delete details", font=("verdana", 20, "bold"))
entrno3 = Entry(dlt, bd=5, font=("verdana", 20, "bold"))
btndlt = Button(dlt, text="Delete record", font=("verdana", 20, "bold"), command=f11)
btndback = Button(dlt, text="Back", font=("verdana", 20, "bold"), command=f8)

lblrno3.pack(pady=15)
entrno3.pack(pady=10)
btndlt.pack(pady=10)
btndback.pack(pady=10)


#=====================================================================================================
# exit 
#=========================

def wd():
	if askokcancel("Quit", "Exit This Tab"):
		root.destroy()

root.protocol("WM_DELETE_WINDOW", wd)

#========================================================================================================
root.mainloop()
