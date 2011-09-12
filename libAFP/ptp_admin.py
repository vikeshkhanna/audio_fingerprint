from Tkinter import *
import tkFileDialog
import os
import sys
import fnmatch
import tkSnack
import MySQLdb
'''
Python GUI wrapper for the fingerprint system 
Alpha version (Developer Testing), AFP v2, May 2011
'''

pad_x = 60
pad_y =15
RECORD_TIME  = 2000
time_since = 0
file_name = 'fp_result'
program = './bin/Debug/libAFP'
MAX_FILES = 20

def run(program, *args):
    pid = os.fork()
    if not pid:
        os.execvp(program, (program,) +  args)
    return os.wait()[0]


class App:
    def __init__(self, master):
	self.is_playing  = False
	self.filename  = None
	self.is_opened = False
	self.filename = None
	self.num_options = 0
	self.options = [ 0 for i in range(0,MAX_FILES)]
	
	self.master = master
        self.frame_toolbar = Frame(master)
        self.frame_toolbar.pack()
	menu = Menu(master)
	master.config(menu=menu)
	tkSnack.initializeSnack(master)
	
	self.snd_main = tkSnack.Sound()	
	
	frame_lower = Frame(master)
	frame_lower.pack(side=BOTTOM)
	
	self.lbl_result = Label(frame_lower,wraplength=300,text="")
	self.lbl_result.pack(side=LEFT)
	
        self.create_buttons(self.frame_toolbar)
	self.create_menu(menu)
	
	self.frame_options = Frame(master)
	self.frame_options.pack()
	lbl_is_copyright = Label(self.frame_options,text='Is Copyright? (y/n)').pack(side=LEFT)
	self.is_copyright = Entry(self.frame_options)
	self.is_copyright.pack(side=LEFT)
	

	lbl_copyright_holder = Label(self.frame_options,text='Copyright Holder').pack(side=LEFT)
	self.copyright_holder = Entry(self.frame_options)
	self.copyright_holder.pack(side=LEFT)

	self.btn_submit	= Button(self.frame_options,text='Submit',command=self.do_submit).pack(side=LEFT)

    #Create buttons
    def create_buttons(self,frame):
	self.btn_playback = Button(frame, text="Playback", command=self.do_playback,state="disabled",padx=pad_x,pady=pad_y)
        self.btn_playback.pack(side=LEFT)

	self.btn_fingerprint = Button(frame, text="Get Fingerprint", command=self.get_fingerprint,state="disabled",padx=pad_x,pady=pad_y)
        self.btn_fingerprint.pack(side=LEFT)
	
	self.btn_match = Button(frame, text="Get Match", command=self.get_match,state="disabled",padx=pad_x,pady=pad_y)
        self.btn_match.pack(side=LEFT)	
 

    #Create Menu
    def create_menu(self,menu):
	menu_file = Menu(menu,tearoff=0)
	menu.add_cascade(label="File", menu=menu_file)
	menu_file.add_command(label="New", command=self.do_initialize)
	menu_file.add_command(label="Open File", command=self.do_open_file)
	menu_file.add_separator()
	menu_file.add_command(label="Exit", command=self.do_exit)
	
	menu_help = Menu(menu,tearoff=0)	
	menu.add_cascade(label="Help", menu=menu_help)
	menu_help.add_command(label="About", command=self.show_about)


    #Playback recoreded/opened audio
    def do_playback(self):
	if self.is_playing:
		self.snd_main.stop()
		self.btn_playback['text'] = 'Playback'
		self.is_playing = False
	else:
		self.snd_main.play()
		self.btn_playback['text'] = 'Stop'
		self.is_playing=True
		#self.master.after(RECORD_TIME,self.do_playback)
		
        print "Playback called!"

    #Fetch only fingerprint	
    def get_fingerprint(self):
	run(program, "-p","--file=fp_result",self.filename)
	run(program, "-p","--file=fp_result",self.filename)
	
	f = open(file_name,'r')
	self.lbl_result['text'] = f.read()		
	f.close()	
		#os.system('./libAFP -p --file=' + file_name + ' fp_temp.wav')         
	print "Get Fingerprint called!"

    #Fetch the audio match
    def get_match(self):
	run(program, "-m","--file=fp_result",self.filename)
	f = open(file_name,'r')	
	self.title = f.readline()
	self.artist = f.readline()
	self.puid = f.readline()
	self.lbl_result['text'] = self.title + ', ' + self.artist	
	f.close()	
        print "Get Match called!"

    #Initialize
    def do_initialize(self):
        print "Do Initialize called!"

    #Initialize
    def do_exit(self):
	root.destroy()
        print "Do exit called!"

    #Show about	
    def show_about(self):
	top = Toplevel()
	top.title("About Floyd Rose P2P Filter")
	about_message = 'Floyd Rose P2P filter was developed by Rishabh Sood, Santosh Kumar and Vikesh Khanna as a part of their BTP (IIT Roorkee)'
	msg = Message(top, text=about_message)
	msg.pack()
	button = Button(top, text="Close", command=top.destroy)
	button.pack()

        print "Show about called!"

    #Open audio clip	
    def do_open_file(self):
	self.filename = tkFileDialog.askopenfilename()

	if self.filename :
		self.btn_playback['state'] = 'active'
		self.btn_match['state'] = 'active'
		self.btn_fingerprint['state'] = 'active'
		self.snd_main.load(self.filename)	
	
	print "Open file called!"

    def do_submit(self):
	conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "vikesh",db = "btp")
	cursor = conn.cursor ()
	command = 'SELECT * from ptp WHERE puid="%s"'%self.puid 
	#print command
	cursor.execute (command)
	row = cursor.fetchone ()

	if self.is_copyright.get()=='y':
		cond=1
	else:
		cond=0
	
	if not row:
		command = 'INSERT INTO ptp VALUES("%s",%d,"%s",0,"%s")'%(self.puid,cond,self.copyright_holder.get(),self.title)
	else:
		command = 'UPDATE ptp SET is_copyright=%d, copyright_holder="%s",title="%s" WHERE puid="%s"'%(cond,self.copyright_holder.get(),self.puid,self.title)
	cursor.execute(command)
	
	cursor.close ()
	conn.close ()
	pass


root = Tk()
root.title(string='Floyd Rose P2P Filter')
app = App(root)
app.width=1000

root.mainloop()

