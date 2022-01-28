try:
	import pywhatkit as pk
except Exception as e:
	print(e)
import requests
from bs4 import BeautifulSoup as bs
import webbrowser as wb
import smtplib
import geopy
import os
import re
import pyjokes
import time
import pyautogui as pg
import wikipedia as wp
from email.message import EmailMessage
from main import ifContain
from dotenv import load_dotenv

load_dotenv()
msg = EmailMessage()

def getSpecificCountry(txt,country):
	for i in txt.split():
		print(i)
		if i in country:
			return country[i],i
	return False,False

class Covid():
	def __init__(self):
		self.URL = "https://www.worldometers.info/coronavirus/"
		self.totalStat = {}
		self.countryStat = {}
		self.soup = None

	def scrapData(self):
		r  = requests.get(self.URL)
		htmlcontent = r.content
		self.soup = bs(htmlcontent,	"html.parser")
		return self.soup

	def getTotalStat(self):
		self.scrapData()
		total = self.soup.find_all("div",class_="maincounter-number")
		self.totalStat = { k:v for (k,v) in zip(["totalCases","totalDeaths","totalRecovered"], [i.span.string for i in total])} 
		return self.totalStat

	def getCountryStat(self):
		self.scrapData()
		country = self.getCountryList()
		names = ['totalCases',  'totalDeaths', 'totalRecovered']
		tbody = self.soup.find_all("tbody")[0]
		country_info = [a.string if a.string is not None else "" for i in tbody.find_all("tr")[8:] for a in i.find_all("td")[2:7:2] ]
		self.countryStat = {x.lower(): {y:z for y, z in zip(names, country_info[ind*len(names):])} for ind, x in enumerate([i for i in country])}
		return self.countryStat


	def getCountryList(self):
		country = [i.string for i in self.soup.find_all("a",class_="mt_a")[:220]]
		country.insert(196,"Cayman Islands")
		country.insert(214,"MS Zaandam")
		return country

	def speakData(self,text):
		self.getCountryStat()
		con_data,con = getSpecificCountry(text,self.countryStat)

		if not con_data: 
			self.getTotalStat()
			if "statistics" in text :
				return f"World Data:\nTotal Cases - {self.totalStat['totalCases']}\nTotal Recovered - {self.totalStat['totalRecovered']}\nTotal Deaths - {self.totalStat['totalDeaths']}"
			if "cases" in text:
					return f"Total Cases in the world are - {self.totalStat['totalCases']}"
			elif "recovered" in text:
				return f"Total people recovered in the world are - {self.totalStat['totalRecovered']}"
			elif ifContain(text,["deaths","died","death"]):
				return f"Total Deaths in the world are - {self.totalStat['totalDeaths']}"
			else:
				return "Please be more specific"
		else:
			if "statistics" in text :
				return f"{con} data:\nTotal Cases - {con_data['totalCases']}\nTotal Recovered - {con_data['totalRecovered']}\nTotal Deaths - {con_data['totalDeaths']}"
			if "cases" in text:
				return f"Total Cases in {con} are - {con_data['totalCases']}"
			elif "recovered" in text:
				return f"Total people recovered in {con} are - {con_data['totalRecovered']}"
			elif ifContain(text,["deaths","died","death"]):
				return f"Total Deaths in {con} are - {con_data['totalDeaths']}"
			else:
				return "Please be more specific"

# class Weather():
# 	def __init__(self):
# 		self.Key = "6025ee3ca46a49ef86c112637222401"
# 		self.URL = "http://api.weatherapi.com/v1"

# 	def getWeatherReport(self):
# 		a = requests.get(self.URL + "/current.json" + "?key="+self.Key)
# 		print(a)
# 		print(a.text)

def getWiki(command):
	try:
		data = wp.summary(command,sentences=1)
		return data
	except Exception as e:
		return "Could Not find information"


def openSite(site):
	wb.open(site)

def getNews(num):
	apiKey = os.getenv("NEWS_API_KEY")
	url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={apiKey}&pageSize=2&page={num}"
	res = requests.get(url)
	return res.json()["articles"]
	


def search(command):	
	wb.open("https://google.com/search?q=" + command)

def openYoutube(command):
	pk.playonyt(command)

def sendEmail(to,subject,text):
	msg.set_content(text)

	msg['Subject'] = subject
	msg['From'] = os.getenv("EMAIL_USERNAME")
	msg['To'] = to
	server = smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	server.login(msg["From"],os.getenv("EMAIL_PASSWORD"))
	server.send_message(msg)
	server.close()


def tellJokes():
	res = requests.get("https://icanhazdadjoke.com/",headers={"Accept": "text/plain"})
	return res.text

def sendWhatsApp(phNo,message):
	wb.open('https://web.whatsapp.com/send?phone='+"+91" +str(phNo)+'&text='+message)
	time.sleep(20)
	pg.press("enter")

def googleMaps(destination):
	wb.open('https://www.google.com/maps/search/'+destination)

