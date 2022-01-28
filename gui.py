from tkinter import *
from main import *
import internet_functions as ifc
class Gui(Tk):
	def __init__(self):
		super().__init__()
		self.geometry("380x600")
		self.BgColor = "#F6FAFB"
		self.widColor = "#23AE79"
		self.bottomBarColor = "#E8EBEF"
		self.botChatBgColor = "#007dc7"
		self.userChatBgColor = "#23AF79"
		self.voice = True
	def chat(self,text,bot=True):
		height = 0
		if bot:
			self.botChat = Label(self.chat_frame,text=text,bg=self.botChatBgColor,justify="left",padx=5,pady=5
								,fg="white",wraplength=255,font="comicsans 11 bold")
			self.botChat.pack(anchor="w",padx=5,pady=10)
			self.botChat.update()
			
			
		else:
			self.userChat = Label(self.chat_frame,text=text,bg=self.userChatBgColor,justify="left",padx=5,pady=5
								,fg="white",wraplength=255,font="comicsans 11 bold")
			self.userChat.pack(anchor="e",padx=30,pady=10)
			self.userChat.update()
			height = self.userChat.winfo_height() + 30
		self.chat_frame.update()

		# print(self.chat_frame.winfo_height())

	def clearChat(self):
		for widget in self.chat_frame.winfo_children():
			widget.destroy()

	def makeWid(self):
		# chat frame
		
		self.chat_frame = Frame(self,width=380,height=500,bg=self.BgColor)
		self.chat_frame.pack_propagate(0)
		self.chat_frame.pack()
		# input mode frame	
		self.voiceMode = Frame(self,width=380,height=100,bg=self.bottomBarColor)
		self.voiceMode.pack()
		self.voiceMode.pack_propagate(0)
		# keyboard img
		self.keyboard_icon = PhotoImage(file="assets/keyboard.png")
		self.switchToKeyboard = Button(self.voiceMode,image=self.keyboard_icon,borderwidth=0,
										command=lambda: self.unpack(self.voiceMode,self.keyboardMode))
		self.switchToKeyboard.pack(padx=20,side=LEFT)	
		# bot status
		self.botStatus = Label(self.voiceMode,text="Listening....",bg=self.widColor,fg="white",padx=15
								,pady=10,font="Verdana 17")
		self.botStatus.pack(padx=10,side=LEFT)
		# keyboard Mode
		self.keyboardMode = Frame(self,width=380,height=100,bg=self.bottomBarColor)
		self.keyboardMode.pack_propagate(0)
		# keyboard image
		self.voice_icon = PhotoImage(file="assets/mic.png")
		self.switchToVoice = Button(self.keyboardMode,image=self.voice_icon,borderwidth=0, 
									command=lambda: self.unpack(self.keyboardMode,self.voiceMode))
		self.switchToVoice.pack(padx=5,side=LEFT)
		self.keyboardInput = Entry(self.keyboardMode,fg="white", bg="#031E25", font="Verdana 13", 
									bd=6, width=25, relief="flat")
		self.keyboardInput.pack(padx=2,side=LEFT)

	def unpack(self,unpack_wid,pack_wid):
		self.keyboardInput.bind('<Return>', self.keyboardMedium)
		unpack_wid.pack_forget()
		pack_wid.pack()


	def changeBotStatus(self,txt):
		self.botStatus.config(text=txt)
		
	def main(self,txt):
		if txt:
			if "joke" in txt:
				self.clearChat()
				self.chat(txt,bot=False)
				joke = ifc.tellJokes()
				self.speak(joke)
				self.speak("Have fun!")
				return
			if "send" in txt:
				self.clearChat()
				self.chat(txt,bot=False)
				if ifContain(txt,gmail_keyword):
					
					self.speak("Please type recipient email!")
					rec = pg.prompt(text='Enter your email', title='Email message sender' , default='')
					self.speak("What should be the subject?")
					title = self.speech()
					self.chat(title,bot=False)

					self.speak("What is the message?")
					msg = self.speech()
					self.chat(msg,bot=False)

					Thread(target=ifc.sendEmail,args=(rec,title,msg,)).start()
					self.speak("Your mail has been delivered")
				
				else:

					self.speak("Please enter the number")
					num = pg.prompt(text='Enter recipient phone number', title='whatsapp message sender' , default='')
					self.speak("what is the message?")
					msg =  self.speech()
					self.chat(msg,bot=False)	
					Thread(target=ifc.sendWhatsApp,args=(num,msg,)).start()
					self.speak("Your message will be sent shortly")
				return
			if ifContain(txt,maps_keyword):
				self.clearChat()
				self.chat(txt,bot=False)
				self.speak("Which place you want to look for?")
				des = self.speech()
				Thread(target=ifc.googleMaps,args=(des,)).start() 
				self.speak("Here you go....")
				
				return 
			if ifContain(txt,youtube_keyword):
				self.clearChat()
				self.chat(txt,bot=False)
				txt = removeFromText(txt,youtube_keyword)
				Thread(target=ifc.openYoutube,args=(txt,)).start()
				self.speak("okay, opening youtube!")
				
				return 
			if ifContain(txt,search_keyword):
				self.clearChat()
				self.chat(txt,bot=False)
				txt = removeFromText(txt,search_keyword)
				Thread(target=ifc.search,args=(txt,)).start()
				self.speak("okay, opening google ")
				return
			if ifContain(txt,wiki_keyword):
				self.clearChat()
				self.chat(txt,bot=False)
				txt = removeFromText(txt,wiki_keyword)
				self.speak("getting information...")
				a = ifc.getWiki(txt)
				self.speak(a)
				return
			if "news" in txt:
				self.clearChat()
				self.chat(txt,bot=False)
				read = False
				with open("newsNum.txt","r") as f:
					num = f.read()
				with open("newsNum.txt","w") as f:
					if num == "":
						f.write("2")
						num = 1
					else:
						num = int(num) + 1
						f.write(str(num))

				a = ifc.getNews(num)
				# self.speak("Do you want me to read the news for you?")
				# res = self.speech()
				# if ifContain(res,["yes","ya","yep","yeah"]): read = True 
				for i in a:
					self.speak(i["title"])
					print("\nVisit the url to read full news" + i["url"])
					print("            ---------------------##################-------------------------")
				
				
				return

			if ifContain(txt,["covid","cornona virus"]):
				self.clearChat()
				self.chat(txt,bot=False)
				c = ifc.Covid()
				self.speak(c.speakData(txt))
				return
			if ifContain(txt,["note","todo","notes","todos"]):
				self.clearChat()
				self.chat(txt,bot=False)
				file = "todo.txt"
				if ifContain(txt,["write","add","make","create"]):
					if not os.path.isfile(file):
						with open(file,"w") as f:
							pass
					with open(file,"a") as f:
						self.speak("what do you want to add?")
						note = False
						while not note:
							res = self.speech()
							if res: 
								f.write(res+"\n")
								self.chat(res,bot=False)
								self.speak("Note Added")

								note = True
								return
							else:
								self.speak("Please repeat the note.")

				elif ifContain(txt,["show","display","give","get","read"]):
					if not os.path.isfile(file): self.speak("You don't have any notes")
					with open(file,"r") as f:
						note = f.readlines()
						print(note)
						l = [f"You have {len(note)}  notes"]
						for i in  note:
							l.append(i)
						print(l)
						for i in l:
							self.speak(i)
				elif ifContain(txt,["delete","remove"]):
					self.speak("All your notes have been deleted")
					with open(file,"w") as f:
						f.write("")
				else:
					self.speak("I was unable to understand you.")
				return			
				
			else:
				self.chat(txt,bot=False)
				self.speak("Sorry, I am unable to understand you. Try something different")
				self.clearChat()
				return

	def speak(self,audio):
		self.changeBotStatus("Speaking....")
		print(f"Bot: {audio}")
		self.chat(audio)
		engine.say(audio)
		engine.runAndWait()
		self.changeBotStatus("Listening....")
	
	def speech(self):
		if self.voice:
			try:
				r = sr.Recognizer()
				r.dynamic_energy_threshold = False
				r.energy_threshold = 4000
				self.changeBotStatus("Listening....")
				
				with sr.Microphone() as src:
					r.adjust_for_ambient_noise(src,duration=1)
					audio = r.listen(src)
				self.changeBotStatus("Processing...")
				command = r.recognize_google(audio)
				print(f"user: {command} \n")
				
				return command.lower()
			except sr.UnknownValueError:
				r = sr.Recognizer()
				# self.speak("Sorry, could you repeat again!")
		else:

			return self.keyboardInput.get()	

	def voiceMedium(self):
		self.voice= True
		while True:
			voice_input = self.speech()
			if ifContain(voice_input,["shutdown","shut down","shut","exit","close","bye","goodbye"]):
				self.chat(voice_input,bot=False)
				self.speak("Bye, closing the app")
				self.destroy()
				break
			else:
				self.main(voice_input)
		exit()
	def keyboardMedium(self,event):
		inp  = self.keyboardInput.get()
		if inp:
			self.voice = False
			Thread(target=self.main,args=(inp,)).start()
			self.chat(inp,bot=False)
			self.keyboardInput.delete(0,END)


if __name__ == '__main__':
	win = Gui()
	win.makeWid()	
	win.speak("Hi, How can I help you?")
	Thread(target=win.voiceMedium).start()
	win.mainloop()
	with open("newsNum.txt","w") as f:
		f.write("")
