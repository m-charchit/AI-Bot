from threading import Thread
import os
import speech_recognition as sr
import pyttsx3
import pyautogui as pg


gmail_keyword = ["gmail","email"]
maps_keyword = ["maps","map","google maps"]
youtube_keyword = ["youtube","play"]
search_keyword = ["search", "on google"]
wiki_keyword = ["wiki","wikipedia","on wikipedia","who","what "]

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('volume', 1)





def removeFromText(txt,lst):
	for i in lst:
		txt  = txt.replace(i,"")
	return txt

def ifContain(txt,lst):
	if txt:
		for i in lst:
			if i in txt:
				return True
		return False
	else:
		return False




