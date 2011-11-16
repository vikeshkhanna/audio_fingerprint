from Tkinter import *
import MySQLdb
import tkFileDialog
import os
import sys
import fnmatch
import tkSnack

'''
Python GUI wrapper for the fingerprint system,
Developed by @Vikesh Khanna in May 2011
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
	self.is_opened = False
	self.filename = None
	self.RADIO_VARIABLE = StringVar()
	self.num_options = 0
	self.options = [ 0 for i in range(0,MAX_FILES)]
	
	self.master = master
        self.frame_toolbar = Frame(master)
        self.frame_toolbar.pack()
	menu = Menu(master)
	master.config(menu=menu)
	tkSnack.initializeSnack(master)
	
	self.snd_main = tkSnack.Sound()	
	
	self.frame_files  = Frame(master)
	self.frame_files.pack(side=LEFT)
	
	frame_lower = Frame(master)
	frame_lower.pack(side=BOTTOM)
	
	self.lbl_result = Label(frame_lower,wraplength=300,text="")
	self.lbl_result.pack(side=LEFT)
	
        self.create_buttons(self.frame_toolbar)
	self.create_menu(menu)
		

    #Create buttons
    def create_buttons(self,frame):
	self.btn_playback = Button(frame, text="Playback", command=self.do_playback,state="disabled",padx=pad_x,pady=pad_y)
        self.btn_playback.pack(side=LEFT)

	self.btn_fingerprint = Button(frame, text="Get Fingerprint", command=self.get_fingerprint,state="disabled",padx=pad_x,pady=pad_y)
        self.btn_fingerprint.pack(side=LEFT)
	
	self.btn_match = Button(frame, text="Share", command=self.get_match,state="disabled",padx=pad_x,pady=pad_y)
        self.btn_match.pack(side=LEFT)	
 

    #Create Menu
    def create_menu(self,menu):
	menu_file = Menu(menu,tearoff=0)
	menu.add_cascade(label="File", menu=menu_file)
	menu_file.add_command(label="New", command=self.do_initialize)
	menu_file.add_command(label="Open File", command=self.do_open_file)
	menu_file.add_command(label="Open Directory", command=self.do_open_directory)
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
		self.snd_main.load(self.RADIO_VARIABLE.get())
		self.snd_main.play()
		self.btn_playback['text'] = 'Stop'
		self.is_playing=True
		#self.master.after(RECORD_TIME,self.do_playback)
		
        print "Playback called!"

    #Fetch only fingerprint	
    def get_fingerprint(self):
	if not self.is_opened:
		run(program, "-p","--file=fp_result",self.RADIO_VARIABLE.get())
		
	else:	
		run(program, "-p","--file=fp_result",self.RADIO_VARIABLE.get())
	
	f = open(file_name,'r')
	self.lbl_result['text'] = f.read()		
	f.close()	
		#os.system('./libAFP -p --file=' + file_name + ' fp_temp.wav')         
	print "Get Fingerprint called!"

    #Fetch the audio match
    def get_match(self):
	if not self.is_opened:
		run(program, "-m","--file=fp_result",self.RADIO_VARIABLE.get())
	else:
		run(program, "-m","--file=fp_result",self.RADIO_VARIABLE.get())
				
	f = open(file_name,'r')
	self.title = f.readline()
	self.artist = f.readline()
	self.puid = f.readline()
	self.lbl_result['text'] = self.title + ' by ' + self.artist		
	f.close()	
	conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "vikesh",db = "btp")
	cursor = conn.cursor ()
	command = 'SELECT * from ptp WHERE puid="%s"'%self.puid 
	#print command
	cursor.execute (command)
	row = cursor.fetchone ()

	if not row or not row[1]:
		self.lbl_result['text'] += '\nThis song is not protected by Copyright. You may download it'
	else:
		self.lbl_result['text'] += str('\nYou cannot share this song as it is a copyright material held by %s'%row[2])
	cursor.close ()
	conn.close ()
	
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
	filename = tkFileDialog.askopenfilename()

	if self.num_options > MAX_FILES:
		tkMessageBox.showwarning(
        		"File Limit Exceeded",
		        "Cannot open more than %d files" % filename
    			)
		
		return 

	if filename :
		self.btn_playback['state'] = 'active'
		self.btn_match['state'] = 'active'
		self.btn_fingerprint['state'] = 'active'
		self.options[self.num_options] = Radiobutton(self.frame_files, text=filename[filename.rfind('/')+1:], variable=self.RADIO_VARIABLE,value=filename).pack(anchor=W)
		self.num_options = self.num_options + 1		
		#self.snd_main.load(self.filename)			
		self.is_opened = True
	print "Open file called!"

    def do_open_directory(self):
 	dirname = tkFileDialog.askdirectory()	

	if dirname:
		self.btn_playback['state'] = 'active'
		self.btn_match['state'] = 'active'
		self.btn_fingerprint['state'] = 'active'
				
		for filename in os.listdir(dirname): #traverse the directory
		    if fnmatch.fnmatch(filename, '*.mp3') or fnmatch.fnmatch(filename,"*.wav"): #filter supported audio files
			if self.num_options<MAX_FILES :
    			        self.options[self.num_options] = Radiobutton(self.frame_files, text=filename, variable=self.RADIO_VARIABLE,value=dirname + '/' + filename).pack(anchor=W)
				self.num_options = self.num_options + 1		
				  	
			#print file
	
		print dirname
	
	print "Open Directory called"

root = Tk()
root.title(string='Floyd Rose P2P Filter')
app = App(root)
app.width=1000

root.mainloop()

