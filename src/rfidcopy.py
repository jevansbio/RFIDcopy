import os
import csv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import *
import shutil as shutil

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit

def quit():
    root.quit()
	
class Application(Frame):

	def __init__(self, master=None, Frame=None):
		
		Frame.__init__(self,master)
		super(Application,self).__init__()
		self.grid(column = 1,row = 5,padx = 50,pady = 10)
		self.master.wm_attributes("-topmost", 1)
		self.master.after(1, lambda: self.master.focus_force())
		self.master.iconbitmap('rfidicon.ico')
		self.type=0
		self.datadir='nan'
		self.id=False
		self.data=False
		self.checkconfig()	
		self.createWidgets()
				
		self.centrewindow(self.master)

	def centrewindow(self,win):
		# Apparently a common hack to get the window size. Temporarily hide the
		# window to avoid update_idletasks() drawing the window in the wrong
		# position.
		win.withdraw()
		win.update_idletasks()  # Update "requested size" from geometry manager

		x = (win.winfo_screenwidth() - win.winfo_reqwidth()) / 2
		y = (win.winfo_screenheight() - win.winfo_reqheight()) / 2
		win.geometry("+%d+%d" % (x, y))

		# This seems to draw the window frame immediately, so only call deiconify()
		# after setting correct window position
		win.deiconify()#
	def checkconfig(self):
		if(os.path.isfile("rfidcopyconfig.cfg")):
			with open('rfidcopyconfig.cfg') as csvFileObj:
					csvRows = []
					readerObj = csv.reader(csvFileObj)
					for row in readerObj:
						csvRows.append(row)
					csvFileObj.close()
					self.drivepath=csvRows[0][0]
					if(self.drivepath==""):
						self.drivepath="D:\\"
					self.datadir1=csvRows[0][1]
					if(self.datadir1==""):
						self.datadir1="Z:\\RFIDDATA2017"
					self.datadir2=csvRows[0][2]
					if(self.datadir2==""):
						self.datadir2="Z:\\SELECTIVERFID2017"
					self.writeconfig()
		else:
			self.drivepath="D:\\"
			self.datadir1="Z:\\RFIDDATA2017"
			self.datadir2="Z:\\SELECTIVERFID2017"
			self.writeconfig()
			
	def writeconfig(self):
		configs=[self.drivepath,self.datadir1,self.datadir2]
		with open("rfidcopyconfig.cfg", 'w',newline='') as csvfile:
			cfgwriter = csv.writer(csvfile)
			cfgwriter.writerow(configs)
	def checksd(self):
		
		try:
			csvRows = []
			csvFileObj = open(self.drivepath+"RFIDID")

			readerObj = csv.reader(csvFileObj,delimiter='\t')
			for row in readerObj:
				if readerObj.line_num == 1:
					continue    # skip first row
				csvRows.append(row)
			csvFileObj.close()
			self.type=csvRows[0][0]
			self.site=csvRows[0][1]
			self.feederid=csvRows[0][2]

			if(self.type=='1'):

				self.datadir=self.datadir1
			elif(self.type=='2'):
				self.datadir=self.datadir2
			self.datadirlabel['text']="Current data dir is: "+self.datadir
			self.sitedirlabel['text']="Current site is: "+self.site
			self.feederidlabel['text']="Current feeder ID is: "+self.feederid
			self.id=True

		except:
			self.id=False
			self.type='0'
			self.site='nan'
			self.feederid='nan'
			self.datadir='nan'
			self.datadirlabel['text']="  "
			self.sitedirlabel['text']="  "
			self.feederidlabel['text']="  "
			self.statuslabel['text']="No ID file found"
	def checkdata(self):

		
		try:
			if(self.type=='1'):
				
				files=os.listdir(self.drivepath)
				selector=([".DAT" in s for s in os.listdir(self.drivepath)])
				self.selectdata=([i for (i, v) in zip(files, selector) if v])[0]
				if(len(self.selectdata)>0):
					with open(self.drivepath+self.selectdata) as csvFileObj:
						csvRows = []
						class rfid_tab(csv.excel):
							delimiter = ' '
							skipinitialspace = True
						csv.register_dialect("rfid_tab", rfid_tab)
						readerObj = csv.reader(csvFileObj, 'rfid_tab')
						
						for row in readerObj:
							csvRows.append(row)
						csvFileObj.close()
					firstentry=csvRows[0][0]
					lastentry=csvRows[len(csvRows)-1][0]
					self.thisentry=firstentry+'_'+lastentry
					self.data=True
			elif(self.type=='2'):
				csvRows = []
				self.selectdata="LOG.TXT"
				csvFileObj = open(self.drivepath+self.selectdata)
				readerObj = csv.reader(csvFileObj)
				for row in readerObj:
					csvRows.append(row)
				csvFileObj.close()
				firstentry=csvRows[0][0]
				lastentry=csvRows[len(csvRows)-1][0]
				self.thisentry=firstentry+'_'+lastentry
				self.thisentry=self.thisentry.replace('/', '')
				self.data=True
			#COPY AND DELETE
			self.statuslabel['text']="Press enter to download"
		except:
			self.statuslabel['text']="No data on SD"
			
	def copydata(self,event=False):
		try:
			if (os.path.exists(self.datadir+'\\'+self.site+'\\'+self.feederid+'\\'+self.thisentry)==False):
				os.makedirs(self.datadir+'\\'+self.site+'\\'+self.feederid+'\\'+self.thisentry)
			shutil.move(self.drivepath+self.selectdata, self.datadir+'\\'+self.site+'\\'+self.feederid+'\\'+self.thisentry+'\\'+self.selectdata)
			self.refreshwidgets()
		except:
			self.statuslabel['text']="ERROR DOWNLOADING DATA"
		
	# def key(self,event):
		# if event.char == event.keysym:
			# msg = 'Normal Key %r' % event.char
		# elif len(event.char) == 1:
			# msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
		# else:
			# msg = 'Special Key %r' % event.keysym
		# print(msg)
	def choose_sd(self):
		drivepath = filedialog.askdirectory(title = "Select SD card drive")
		if(drivepath!=""):
			self.drivepath=drivepath
		self.writeconfig()
		
	def choose_datafolder1(self):
		datadir1 = filedialog.askdirectory(title = "Select folder")
		if(datadir1!=""):
			self.datadir1=datadir1
		self.writeconfig()
	def choose_datafolder2(self):
		datadir2 = filedialog.askdirectory(title = "Select folder")
		if(datadir2!=""):
			self.datadir2=datadir2		
		self.writeconfig()
	def createWidgets(self):
		self.menubar = Menu(self)
		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="File", menu=menu)
		menu.add_command(label="Choose SD card drive",command=self.choose_sd)
		menu.add_command(label="Choose RFID data folder",command=self.choose_datafolder1)
		#menu.add_command(label="Choose selective feeder folder",command=self.choose_datafolder2)
		try:
			self.master.config(menu=self.menubar)
		except AttributeError:
			# master is a toplevel window (Python 1.4/Tkinter 1.63)
			self.master.tk.call(master, "config", "-menu", self.menubar)		

		self.sdlabel=Label(text=("Current SD card drive is "+self.drivepath),width=35)
		self.sdlabel.grid(column=1, row=0, sticky=(W))
		
		self.datadirlabel=Label(text=" ",width=35)
		self.datadirlabel.grid(column=1, row=1, sticky=(W))
		self.sitedirlabel=Label(text=" ",width=35)
		self.sitedirlabel.grid(column=1, row=2, sticky=(W))
		self.feederidlabel=Label(text=" ",width=35)
		self.feederidlabel.grid(column=1, row=3, sticky=(W))
		self.statuslabel=Label(text=" ",width=35)
		self.statuslabel.grid(column=1, row=4, sticky=(N),pady=10)
		self.cdbutton=ttk.Button(text='Move data', width=18, state=DISABLED,master=self.master,command=self.copydata)
		self.cdbutton.grid(column=1, row=5, sticky=(N),pady=10)
		self.refreshwidgets()
	def refreshwidgets(self):
		self.sdlabel['text']=("Current SD card drive is "+self.drivepath)
		self.checksd()
		if(self.id==True):
			
			self.checkdata()
			if(self.data==True):
				self.cdbutton.state(["!disabled"])
				self.master.bind('<Return>', self.copydata)
			else:
				self.master.unbind('<Return>')
		self.after(1000, self.refreshwidgets)
root = Application()
root.master.title("Copy from SD")


root.mainloop()			
