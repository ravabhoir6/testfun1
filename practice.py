from msilib import add_data
from multiprocessing import connection
import tkinter  as tk 
from tkinter import *
import MySQLdb as mdb
from sqlalchemy import create_engine

my_w = tk.Tk()
my_w.geometry("450x350") 
global i
user = 'root'
password = ''
host = 'localhost'
port = 3306
database = 'newform'
  
# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
my_conn=create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
def display():
    my_cursor=my_conn.execute("SELECT * FROM practice limit 0,10")
    global i
    i=0 
    for student in my_cursor: 
        for j in range(len(student)):
            e = Label(my_w,width=10, text=student[j],
                relief='ridge', anchor="w")  
            e.grid(row=i, column=j) 
            #e.insert(END, student[j])
        e = tk.Button(my_w,width=5, text='Edit',relief='ridge',
             anchor="w",command=lambda k=student[0]:edit_data(k))  
        e.grid(row=i, column=5)     
        i=i+1
display()
def edit_data(id): # display to edit and update record
    global i # start row after the last line of display
    #collect record based on id and present for updation. 
    row=my_conn.execute("SELECT * FROM practice WHERE id=%s",id)
    s = row.fetchone() # row details as tuple

    e1_str_id=tk.StringVar(my_w) # String variable 
    e2_str_name=tk.StringVar(my_w)
    e3_str_email=tk.StringVar(my_w)


    e1_str_id.set(s[0]) # id is stored 
    e2_str_name.set(s[1]) # Name is stored 
    e3_str_email.set(s[2]) # class is stored 

        
    e1=tk.Entry(my_w,textvariable=e1_str_id,width=10)
    e1.grid(row=i,column=0)
    e2=tk.Entry(my_w,textvariable=e2_str_name,width=10)
    e2.grid(row=i,column=1)
    e3=tk.Entry(my_w,textvariable=e3_str_email,width=10)
    e3.grid(row=i,column=2)
    b2 = tk.Button(my_w,text='Update',command=lambda: my_update(),
                relief='ridge', anchor="w",width=5)  
    b2.grid(row=i, column=5) 
    def my_update(): # update record 
        data=(e1_str_id.get(),e2_str_name.get(),e3_str_email.get())
        print(type(data[0]))
        id=my_conn.execute("UPDATE practice SET name='{1}', email='{2}' WHERE id={0}".format(data[0], data[1], data[2]))
        print("Row updated  = ",id.rowcount) 
        for w in my_w.grid_slaves(i): # remove the edit row
            w.grid_forget()
        display()  # refresh the data

        
btnAdd = tk.Button(my_w,text='Add',command=lambda: add_data(),
                relief='ridge', anchor="w",width=15)  
btnAdd.place(x=150, y=250)
def add_data():  
    e1_str_id=tk.StringVar(my_w) # String variable 
    e2_str_name=tk.StringVar(my_w)
    e3_str_email=tk.StringVar(my_w)

    e1=tk.Entry(my_w,textvariable=e1_str_id,width=10)
    e1.grid(row=i,column=0)
    e2=tk.Entry(my_w,textvariable=e2_str_name,width=10)
    e2.grid(row=i,column=1)
    e3=tk.Entry(my_w,textvariable=e3_str_email,width=10)
    e3.grid(row=i,column=2)
    b2 = tk.Button(my_w,text='add',command=lambda: my_add(),
                relief='ridge', anchor="w",width=5)  
    b2.grid(row=i, column=5) 
    def my_add():
        data =  data=(e1_str_id.get(),e2_str_name.get(),e3_str_email.get())
        adding = my_conn.execute("INSERT INTO practice (id, name, email)VALUES ({0}, '{1}', '{2}')".format(data[0], data[1], data[2]))
        print("Row added = ", adding.rowcount) 
        for w in my_w.grid_slaves(i): # remove the edit row
            w.grid_forget()
        display()  
my_w.mainloop()