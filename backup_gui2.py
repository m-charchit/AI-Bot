from tkinter import *

class Gui(Tk):
	def __init__(self):
		super().__init__()
		self.geometry("380x600")
		self.BgColor = "#F6FAFB"
		self.widColor = "#23AE79"
		self.bottomBarColor = "#E8EBEF"
		self.botChatBgColor = "#007dc7"
		self.userChatBgColor = "#23AF79"
		self.medium = "voice"
	def chat(self,text,bot=True):
		height = 0
		if bot:
			self.botChat = Label(self.chat_frame,text=text,bg=self.botChatBgColor,justify="left",padx=5,pady=5
								,fg="white",wraplength=255,font="comicsans 11 bold")
			self.botChat.pack(anchor="w",padx=5,pady=10)
			self.botChat.update()
			print(self.botChat.winfo_height() + 30)
			
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
										command=lambda: self.unpack(self.voiceMode,self.keyboardMode,"keyboard"))
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
									command=lambda: self.unpack(self.keyboardMode,self.voiceMode,"voice"))
		self.switchToVoice.pack(padx=5,side=LEFT)
		self.keyboardInput = Entry(self.keyboardMode,fg="white", bg="#031E25", font="Verdana 13", 
									bd=6, width=25, relief="flat")
		self.keyboardInput.pack(padx=2,side=LEFT)

	def unpack(self,unpack_wid,pack_wid,medium):
		self.medium = medium
		self.keyboardInput.bind('<Return>', self.enter)
		unpack_wid.pack_forget()
		pack_wid.pack()

	def enter(self,event):
		from main import voiceMedium
		voiceMedium()
	def changeBotStatus(self,txt):
		self.botStatus.config(text=txt)
		


