import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from os import *
import sqlite3
import subprocess
from subprocess import *
import threading
import pty
import time
class thread(threading.Thread):
    def __init__(self,root,id,name):
        threading.Thread.__init__(self)
        self.threadID=id
        self.name=name
        self.root=root
        self.master,self.slave=pty.openpty()
        self.exe=subprocess.Popen(['./x2'],shell=True,stdout=self.slave,stdin=PIPE)
        self.stdin_handle=self.exe.stdin
        self.stdout_handle=os.fdopen(self.master)

    def run(self):
        print("Starting thread: "+self.name)

        while True:
            print("reading next line from pipe..")
            x=self.stdout_handle.readline()
            if x==b'':
                break
            self.root.console.insert(END,x)
            print(x)
            if '?' in x:
                #t.insert(END,x)
                print("inside t!")
                print(x)
                self.send()

            root.update_idletasks()
            time.sleep(1)
        print("out of loop!")


    def send(self):

        while not self.root.e.get():
            pass
        #print(b'{}'.format(str.encode(e.get())))
        #exe.stdin.open()
        self.stdin_handle.flush()
        self.stdin_handle.write(b''+str.encode(self.root.e.get()))
        self.root.e.delete(0,END)
        self.stdin_handle.flush()
        print("data sent to pipe")
        #t.insert(END,stdout_handle.readline())
        self.stdin_handle.close()
        #print(exe.stdout.readline())
        self.run()


class Application(Frame):
    def __init__(self,root):
        super(Application,self).__init__(root)
        self.config(bg='blue')
        self.grid()
        self.col=2
        self.i=0
        #self.index=2
        #self.isSelected=False
        self.dic={}
        self.type_li=[]
        self.device_li=[]
        self.conn=sqlite3.connect("server_driver.db")
        self.cursor=self.conn.cursor()
        self.host=os.popen("hostname").readlines()
        #print(self.host)
        for i in self.host:
            i=i[:len(i)-1]
            self.type=i
        #print(self.type)
        self.create_widgets()


    def create_widgets(self):
        self.top_frame=Frame(self,width=1900,height=100,relief='raised')
        self.top_frame['bg']='red'

        self.bottom_frame=Frame(self,width=1500,height=100)
        self.bottom_frame.grid(row=17,column=0,columnspan=20,rowspan=5,sticky='nsew')
        self.top_frame.grid(row=0,column=0,columnspan=200,rowspan=4,sticky='nsew')
        self.top_frame.grid_columnconfigure(0,weight=1)
        self.bottom_frame.grid_columnconfigure(0,weight=1)
        Label(self.top_frame,text="Seg2 Tape",fg='yellow',bg='red',font=('Courier',44)).pack(expand=True,fill=BOTH,side='top')
        self.status_txt=Text(self,width=40,height=8,state='disabled',highlightbackground='black',highlightthickness=3,wrap=WORD)
        self.status_txt.grid(row=4,column=0)
        self.cursor.execute("select dname from serv_driv where sname='%s'"%(self.type))
        #print("select dname from serv_driv where sname='%s'"%(self.type))
        self.but_arr1=[]
        #print(self.cursor)
        for row in self.cursor:
            #print(row)
            #print(self.host)
            self.device_li.append(row[0])
            #self.but_arr1.append(Button(self,text=row[0],command=lambda c=self.i:self.printStatus(self.but_arr1[c].cget("text")),fg='purple',bg='yellow'))
            #self.but_arr1[self.i].grid(row=4,column=self.col)
            #self.i+=1
            #self.col+=1
            #self.dic[row[0]]=self.but_arr1

        #print(self.dic)
        '''self.but_arr2=Button(self,text="nst2",command=lambda :self.printStatus("nst2"))
        self.but_arr2.grid(row=0,column=5)
        self.dic["nst2"]=self.but_arr2'''
        Label(self,text="Select Driver: ",font=('bold')).grid(row=4,column=2)

        self.dc=ttk.Combobox(self,values=self.device_li,state='normal')
        self.dc.grid(row=4,column=3)
        Button(self,text="Clear",command=self.clear_status,bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=4,column=1)
        Button(self,text='Run Driver',command=lambda : self.printStatus(),bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=4,column=4)
        self.col+=1
        self.wp=PanedWindow(self)
        Label(self,text="Driver options:",font=('bold')).grid(row=5,column=5)
        Button(self,text="Add driver:",command=lambda : self.add_button(self.tf.get()),bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=6,column=5)
        Button(self,text="Remove driver:",command=lambda :self.del_button(self.tfr.get()),bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=7,column=5)
        self.tf=Entry(self,highlightthickness=3)
        self.tfr=ttk.Combobox(self,values=[],state='normal')
        self.tf.grid(row=6,column=6)
        self.tfr.grid(row=7,column=6)
        self.open_btn=Button(self,text="open file",command=self.choose_file,bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=5,column=0)
        #Label(self,text="open file:").grid(row=5,column=5)
        self.inputfile=Entry(self,highlightthickness=3)
        self.inputfile.grid(row=5,column=2)
        Label(self,text="Record length:",font=('bold')).grid(row=6,column=0)
        self.record=Entry(self,highlightthickness=3)
        self.record.grid(row=6,column=2)
        Label(self,text="sample interval:",font=('bold')).grid(row=7,column=0)
        self.sample=Entry(self,highlightthickness=3)
        self.sample.grid(row=7,column=2)
        Label(self,text="log file:",font=('bold')).grid(row=8,column=0)
        self.log=Entry(self,highlightthickness=3)
        self.log.grid(row=8,column=2)
        Label(self,text="Data type:",font=('bold')).grid(row=9,column=0)
        Label(self,text="Device:",font=('bold')).grid(row=10,column=0)
        Label(self,text="console output:",font=('bold')).grid(row=13,column=0)
        self.console=tkst.ScrolledText(self.bottom_frame,width=75,height=8,state='disabled',highlightbackground='black',highlightthickness=3,wrap=WORD)

        self.console.pack(expand=True,fill=BOTH,side='top')
        #self.cursor.execute("select distinct sname from serv_driv")
        #for n in self.cursor:
        #    self.type_li.append(n)
        self.type_combo=ttk.Combobox(self,values=[1,2,3,4,5,6,7],state='normal')


        #print(self.host)
        #self.type_combo.insert(0,self.type)
        #self.type_combo.config(state='disabled')
        self.type_combo.grid(row=9,column=2)

        #Button(self,text="Update Devices!",command=lambda :self.showDevices(self.type_combo.get())).grid(row=9,column=3)
        self.device_combo=ttk.Combobox(self,state='normal')
        self.showDevices(self.type)
        self.device_combo.grid(row=10,column=2)
        Button(self,text="seg2 tape",command=lambda : self.showOutput(self.inputfile.get(),self.record.get(),self.sample.get(),self.log.get(),self.type_combo.get(),self.device_combo.get()),bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=13,column=3)
        Button(self,text='Clear',command=self.clear2,bg='yellow',fg='black',font=('Courier',11,'bold')).grid(row=13, column=2)
        Label(self,text="send command: ",font=('bold')).grid(row=13,column=4)
        self.e=Entry(self,highlightthickness=3,highlightbackground='black')
        self.e.grid(row=13,column=5)

    def printStatus(self):
        st=self.dc.get()
        s=os.popen("./saransh_cartridge.octet-stream "+st).readlines()
        self.status_txt.config(state='normal')
        self.status_txt.delete(0.0,END)
        for x in s:
            self.status_txt.insert(0.0,x)
        self.status_txt.config(state='disabled')
    def showOutput(self,i,r,t,l,ty,dev):
        self.console.config(state='normal')
        t1=thread(self,1,'t1')
        t1.start()
        #print(i+r+t+l+ty+dev)
        '''try:
            if int(r)>=1000 and int(r)<=30000 and int(t)>=1 and int(t)<=10 :
                s2=os.popen("./saransh_test_binary.octet-stream "+" "+i+" "+r+" "+t+" "+l+" "+dev+" "+ty).readlines()
                # print(system('ps -C "saransh_test_binary.octet-stream" -o pid='))
                #self.device_li.clear()
                self.device_combo.delete(0,END)
                #self.device_combo.config(state='disabled')
                self.tfr.delete(0,END)
                #self.tfr.config(state='disabled')
                self.console.config(state='normal')
                self.console.delete(0.0,END)
                for x in s2:
                    self.console.insert(0.0,x)
                self.console.config(state='disabled')

                #if i==null or l==null:
                    #messagebox.showerror("Error","please fill all the data entries!")
            elif int(r) not in range(1000,30000):
                messagebox.showerror("Error","Please enter record length between 1000 and 30000!")
            else:
                messagebox.showerror("Error","Sample interval has to be within 1 and 10 ms")
        except:
            messagebox.showerror("Error","please fill all the data entries!")'''



        #print(system('ps -C "python3 hello.py" -o pid='))
        # print(system('ps -q 256 -o comm='))
    def choose_file(self):
        self.fname =filedialog. askopenfilename(filetypes=(("Template files", "*.tplate"),("HTML files", "*.html;*.htm"),("All files", "*.*") ))
        if self.fname:
            self.inputfile.insert(0,self.fname)

    def add_button(self,name):

        try:

            self.cursor.execute("insert into serv_driv values(?,?)",(self.type,name))
            self.conn.commit()
            self.tf.delete(0,END)
            self.device_li.append(name)
            messagebox.showinfo("Message","Driver added successfully!")
            self.showDevices(self.type)
            #self.tfr.config(state='disabled')
        except:
            messagebox.showinfo("Oops!","Driver already exists!")

        #self.index+=1
    def del_button(self,name):
        if messagebox.askokcancel("Delete message","Are you sure to delete it?"):
            self.cursor.execute("delete from serv_driv where sname='%s' and dname='%s'"%(self.type,name))
            print("data removed from table!")
            self.conn.commit()

            self.tfr.delete(0,END)
            #self.tfr.config(state='disabled')

            self.device_li.remove(name)
            self.showDevices(self.type)
        else:
            pass

    def showDevices(self,name):
        '''self.cursor.execute("select dname from serv_driv  where sname='%s'"%(name))
        if len(self.device_li)==0:
            for i in self.cursor:
                self.device_li.append(i)#print(self.type_combo.get())'''

        self.device_combo.config(state='normal')
        self.device_combo.config(values=self.device_li)
        self.tfr.config(state='normal')
        self.tfr.config(values=self.device_li)
        self.dc.config(values=self.device_li)
    def clear_status(self):
        self.status_txt.config(state='normal')
        self.status_txt.delete(0.0,END)
        self.status_txt.config(state='disabled')
    def clear2(self):
        print("here")
        self.console.config(state='normal')
        self.console.delete(0.0,END)
        self.console.config(state='disabled')




window_start_x=(1000/2)
window_start_y=(500/2)
root=Tk()
root.title("GUI")
root.geometry("+%d+%d" % (window_start_x,window_start_y))
root.resizable(False,False)
app=Application(root)
root.configure(bg='blue')
root.mainloop()
