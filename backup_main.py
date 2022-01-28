from threading import Thread
import os
import speech_recognition as sr
import pyttsx3
import internet_functions as ifc
from gui import *
from voice import *
import pyautogui as pg

win = Gui()
win.makeWid()
gmail_keyword = ["gmail","email"]
maps_keyword = ["maps","map","google maps"]
youtube_keyword = ["youtube","play"]
search_keyword = ["search", "on google"]
wiki_keyword = ["wiki","wikipedia","on wikipedia","who is","what is"]

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('volume', 1)



def speak(audio):
	win.changeBotStatus("Speaking....")
	print(f"Bot: {audio}")
	win.chat(audio)
	engine.say(audio)
	engine.runAndWait()
	win.changeBotStatus("Listening....")
	
def speech():
	try:
		r = sr.Recognizer()
		r.dynamic_energy_threshold = False
		r.energy_threshold = 4000
		print("\n listening...")
		with sr.Microphone() as src:
			r.adjust_for_ambient_noise(src,duration=1)
			audio = r.listen(src)
		win.changeBotStatus("Processing...")
		command = r.recognize_google(audio)
		print(f"user: {command} \n")
		win.chat(command,bot=False)
		return command.lower()
	except sr.UnknownValueError:
		r = sr.Recognizer()
		# speak("Sorry, could you repeat again!")

def removeFromText(txt,lst):
	for i in lst:
		txt  = txt.replace(i,"")
	return txt

def main(txt):
	if txt:
		if "joke" in txt:
			speak("Here goes your joke")
			joke = ifc.tellJokes()
			speak(joke)
			win.clearChat()
			return
		if "send" in txt:
			if ifContain(txt,gmail_keyword):
				speak("Please type recipient email!")
				rec = pg.prompt(text='Enter you email', title='Email message sender' , default='')
				speak("What should be the subject?")
				title = speech()
				speak("What is the message?")
				msg = speech()
				Thread(target=ifc.sendEmail,args=(rec,title,msg,)).start()
				speak("Your mail has been delivered")
			
			else:
				speak("Please enter the number")
				num = pg.prompt(text='Enter recipient phone number', title='whatsapp message sender' , default='')
				speak("what is the message?")
				msg =  speech()
				Thread(target=ifc.sendWhatsApp,args=(num,msg,)).start()
				speak("Your message will be sent shortly")
			win.clearChat()
			return
		if ifContain(txt,maps_keyword):
			speak("Which place you want to look for?")
			des = speech()
			Thread(target=ifc.googleMaps,args=(des,)).start() 
			speak("Here you go....")
			win.clearChat()
			return 
		if ifContain(txt,youtube_keyword):
			txt = removeFromText(txt,youtube_keyword)
			Thread(target=ifc.openYoutube,args=(txt,)).start()
			speak("Your video is on your way")
			win.clearChat()
			return 
		if ifContain(txt,search_keyword):
			txt = removeFromText(txt,search_keyword)
			Thread(target=ifc.search,args=(txt,)).start()
			win.clearChat()
			return
		if ifContain(txt,wiki_keyword):
			txt = removeFromText(txt,wiki_keyword)
			speak("getting information...")
			a = ifc.getWiki(txt)
			speak(a)
			win.clearChat()
			return
		if "news" in txt:
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
			speak("Do you want me to read the news for you?")
			res = speech()
			if ifContain(res,["yes","ya","yep","yeah"]): read = True 
			for i in a:
				if read: speak(i["title"])
				else: win.chat(i["title"])
				print("\nVisit the url to read full news" + i["url"])
				print("            ---------------------##################-------------------------")
			win.clearChat()
			return

		if ifContain(txt,["covid","cornona virus"]):
			c = ifc.Covid()
			speak(c.speakData(txt))
			win.clearChat()
		else:
			speak("Sorry, I am unable to reply you.")

def voiceMedium():
	if win.medium == "voice":
		while True:
			if win.medium!="":return
			main(speech())
		
	else:
		inp = win.keyboardInput.get()
		Thread(target=main,args=(inp,)).start()

if __name__ == '__main__':
	
	
	speak("Hi, How can I help you?")
	Thread(target=voiceMedium).start()
	win.mainloop()
	with open("newsNum.txt","w") as f:
		f.write("")

