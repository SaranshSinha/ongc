import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext as tkst
from os import *
class Application(Frame):
    def __init__(self,root):
        super(Application,self).__init__(root)
        self.grid()
        self.col=3
        self.index=2
        self.isSelected=False
        self.create_widgets()


    def create_widgets(self):
        self.status_txt=Text(self,width=40,height=8,state='disabled',wrap=WORD)
        self.status_txt.grid(row=0,column=0)
        self.but_arr1=Button(self,text="nst1",command=lambda :self.printStatus("nst1")).grid(row=0,column=4)
        self.but_arr2=Button(self,text="nst2",command=lambda :self.printStatus("nst2")).grid(row=0,column=5)
        Button(self,text="Add driver:",command=lambda : self.add_button(self.tf.get())).grid(row=3,column=5)
        Button(self,text="Remove driver:",command=self.del_button).grid(row=4,column=5)
        self.tf=Entry(self)
        self.tf.grid(row=3,column=6)
        self.open_btn=Button(self,text="open file",command=self.choose_file).grid(row=5,column=0)
        Label(self,text="open file:").grid(row=5,column=5)
        self.inputfile=Entry(self)
        self.inputfile.grid(row=5,column=6)
        Label(self,text="Record length:").grid(row=6,column=0)
        self.record=Entry(self)
        self.record.grid(row=6,column=2)
        Label(self,text="sample interval:").grid(row=7,column=0)
        self.sample=Entry(self)
        self.sample.grid(row=7,column=2)
        Label(self,text="log file:").grid(row=8,column=0)
        self.log=Entry(self)
        self.log.grid(row=8,column=2)
        Label(self,text="Data type:").grid(row=9,column=0)
        Label(self,text="Device:").grid(row=10,column=0)
        Label(self,text="console output:").grid(row=13,column=0)
        self.console=tkst.ScrolledText(self,width=50,height=8,state='disabled',wrap=WORD)
        self.console.grid(row=14,column=0)
        self.type_combo=ttk.Combobox(self,values=["a","b","c"])
        self.type_combo.grid(row=9,column=2)
        self.device_combo=ttk.Combobox(self,values=["1","2","3"])
        self.device_combo.grid(row=10,column=2)
        Button(self,text="seg2 tape",command=lambda: self.showOutput(self.inputfile.get(),self.record.get(),self.sample.get(),self.log.get(),self.type_combo.get(),self.device_combo.get())).grid(row=10,column=5)


    def printStatus(self,st):
        s=os.popen("./saransh_cartridge.octet-stream "+st).readlines()
        self.status_txt.config(state='normal')
        for x in s:
            self.status_txt.insert(0.0,x)
        self.status_txt.config(state='disabled')
    def showOutput(self,i,r,t,l,ty,dev):

        s2=os.popen("./saransh_test_binary.octet-stream "+" "+i+" "+r+" "+t+" "+l+" "+ty+" "+dev).readlines()
        # print(system('ps -C "saransh_test_binary.octet-stream" -o pid='))

        self.console.config(state='normal')
        for x in s2:
            self.console.insert(0.0,x)
        self.console.config(state='disabled')
        #print(system('ps -C "python3 hello.py" -o pid='))
        # print(system('ps -q 256 -o comm='))
    def choose_file(self):
        self.fname =filedialog. askopenfilename(filetypes=(("Template files", "*.tplate"),("HTML files", "*.html;*.htm"),("All files", "*.*") ))
        if self.fname:
            self.inputfile.insert(0,self.fname)

    def add_button(self,name):
        self.but_arr=Button(self,text=name,command=lambda :self.printStatus(name)).grid(row=1,column=self.col)
        self.col+=1
        self.index+=1
    def del_button(self):
        if self.isSelected==False:
            self.isSelected=True
        else:
            self.isSelected=False


root=Tk()
root.title("GUI")
root.geometry("1080x780")
root.resizable(False,False)
app=Application(root)
root.mainloop()
