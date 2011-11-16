from Tkinter import *
import tkSnack

'''
Python GUI wrapper for the fingerprint system 
Alpha version (Developer Testing), AFP v1, May 2011
'''

pad_x = 60
pad_y =15
RECORD_TIME  = 2000
time_remaining = RECORD_TIME

class App:
    def __init__(self, master):
	self.is_playing  = False
	self.master = master
        self.frame_toolbar = Frame(master)
        self.frame_toolbar.pack()
	menu = Menu(master)
	master.config(menu=menu)
	tkSnack.initializeSnack(master)
	
	self.snd_main = tkSnack.Sound()	
	self.frame_wave = Frame(master)
	self.frame_wave.pack(side=LEFT)

	self.lbl_remaining = Label(master,text="")
	self.lbl_remaining.pack(side=LEFT)
	self.sc = tkSnack.SnackCanvas(self.frame_wave, height=400)
	self.sc.pack(side=LEFT)
	self.sc.create_waveform(0, 0, sound=self.snd_main, height=100, zerolevel=1)
	self.sc.create_spectrogram(0, 150, sound=self.snd_main, height=200)
	
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
		
        print "Playback called!"

    #Listen for/record audio	
    def do_listen(self):
	#print self.snd_main
	global time_remaining
	self.snd_main.record()   
	self.master.after(RECORD_TIME,self.stop_recording)  
	time_remaining = RECORD_TIME/1000
	self.update_timer()
	#self.snd_main.read('/home/vikesh/Desktop/track.wav')	
	#self.snd_main.play()
	print "Listen called!"


    def update_timer(self):
	global time_remaining
	if time_remaining > 0:
		self.lbl_remaining['text'] = 'Recording for another : ' + str(time_remaining) + ' seconds.'
		time_remaining = time_remaining - 1
		self.master.after(1000,self.update_timer)    

    #stop recording
    def stop_recording(self):
	self.lbl_remaining['text'] = 'Recording completed'
	self.snd_main.stop()
	self.btn_playback['state'] = 'active'
	self.btn_match['state'] = 'active'
	self.btn_fingerprint['state'] = 'active'	
	#self.snd_main.play()
	
	print "Stop recording called!"
    
    #Fetch only fingerprint	
    def get_fingerprint(self):
	self.snd_main.write('fpTemp.wav')
        print "Get Fingerprint called!"

    #Fetch the audio match
    def get_match(self):
        print "Get Match called!"

    #Initialize
    def do_initialize(self):
        print "Do Initialize called!"

    #Initialize
    def do_exit(self):
        print "Do exit called!"

    #Show about	
    def show_about(self):
        print "Show about called!"

    #Open audio clip	
    def do_open(self):
        print "Open clip called!"
	

root = Tk()
app = App(root)
app.width=1000

root.mainloop()

