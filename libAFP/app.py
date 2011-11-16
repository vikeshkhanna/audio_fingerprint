from Tkinter import *
import tkFileDialog
import os
import sys
import tkSnack

'''
Python GUI wrapper for the fingerprint system 
Alpha version (Developer Testing), AFP v1, May 2011
'''

pad_x = 60
pad_y =15
RECORD_TIME  = 2000
time_since = 0
file_name = 'fp_result'
program = './bin/Debug/libAFP'



def run(program, *args):
    pid = os.fork()
    if not pid:
        os.execvp(program, (program,) +  args)
    return os.wait()[0]


class App:
    def __init__(self, master):
	self.is_playing  = False
	self.is_listening = False
	self.is_opened = False
	self.filename = None

	self.master = master
        self.frame_toolbar = Frame(master)
        self.frame_toolbar.pack()
	menu = Menu(master)
	master.config(menu=menu)
	tkSnack.initializeSnack(master)
	
	self.snd_main = tkSnack.Sound()	
	self.frame_wave = Frame(master)
	self.frame_wave.pack(side=LEFT)

	self.sc = tkSnack.SnackCanvas(self.frame_wave, height=400)
	self.sc.pack(side=LEFT)
	self.sc.create_waveform(0, 0, sound=self.snd_main, height=100, zerolevel=1)
	self.sc.create_spectrogram(0, 150, sound=self.snd_main, height=200)
	
	frame_lower = Frame(master)
	frame_lower.pack(side=BOTTOM)
	self.lbl_remaining = Label(frame_lower,text="")
	self.lbl_remaining.pack(side=LEFT)
	
	self.lbl_result = Label(frame_lower,wraplength=250,text="")
	self.lbl_result.pack(side=LEFT)
	

        self.create_buttons(self.frame_toolbar)
	self.create_menu(menu)
		

    #Create buttons
    def create_buttons(self,frame):
	self.btn_listen = Button(frame, text="Listen", fg="red", command=self.do_listen, padx=pad_x,pady=pad_y)
        self.btn_listen.pack(side=LEFT)

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
	menu_file.add_command(label="Open", command=self.do_open)
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

    #Listen for/record audio	
    def do_listen(self):
	global time_since

	if not self.is_listening:
		self.is_listening = True
		self.snd_main.record()
		self.btn_listen['text'] = 'Stop'
		time_since = 0		
		self.update_timer()
	else:
		self.is_listening = False
		self.btn_listen['text'] = 'Listen'
		self.stop_recording()
		#print self.snd_main
		
	#self.snd_main.read('/home/vikesh/Desktop/track.wav')	
	#self.snd_main.play()
	print "Listen called!"


    def update_timer(self):
	global time_since
	if self.is_listening:
		self.lbl_remaining['text'] = 'Recorded ' + str(time_since) + ' seconds.'
		time_since = time_since + 1
		self.master.after(1000,self.update_timer)    

    #stop recording
    def stop_recording(self):
	self.is_opened= False
	self.snd_main.write('fp_temp.wav')
	self.lbl_remaining['text'] = 'Recording completed (' + str(time_since) + ' seconds )'
	self.snd_main.stop()
	self.btn_playback['state'] = 'active'
	self.btn_match['state'] = 'active'
	self.btn_fingerprint['state'] = 'active'	
	#self.snd_main.play()
	
	print "Stop recording called!"
    
    #Fetch only fingerprint	
    def get_fingerprint(self):
	if not self.is_opened:
		run(program, "-p","--file=fp_result","fp_temp.wav")
		
	else:	
		run(program, "-p","--file=fp_result",self.filename)
	
	f = open(file_name,'r')
	self.lbl_result['text'] = f.read()		
	f.close()	
		#os.system('./libAFP -p --file=' + file_name + ' fp_temp.wav')         
	print "Get Fingerprint called!"

    #Fetch the audio match
    def get_match(self):
	if not self.is_opened:
		run(program, "-m","--file=fp_result","fp_temp.wav")
	else:
		run(program, "-m","--file=fp_result",self.filename)
				
	f = open(file_name,'r')
	self.lbl_result['text'] = f.read()		
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
	top.title("About Floyd Rose Acoustic Monitor")
	about_message = 'Floyd Rose Acoustic Monitor was developed by Rishabh Sood, Santosh Kumar and Vikesh Khanna as a part of their BTP (IIT Roorkee)'
	msg = Message(top, text=about_message)
	msg.pack()
	button = Button(top, text="Close", command=top.destroy)
	button.pack()

        print "Show about called!"

    #Open audio clip	
    def do_open(self):
	self.filename = tkFileDialog.askopenfilename()

	if self.filename:
		self.btn_playback['state'] = 'active'
		self.btn_match['state'] = 'active'
		self.btn_fingerprint['state'] = 'active'
		self.snd_main.load(self.filename)			
		self.is_opened = True
	print "Open clip called!"
	

root = Tk()
root.title(string='Floyd Rose Acoustic Monitor')
app = App(root)
app.width=1000

root.mainloop()

