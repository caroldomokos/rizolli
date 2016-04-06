#!/usr/bin/python
# load the modules to download http, parse it and to send emails
import requests, bs4
import smtplib
import json
import os
import codecs # this is needed because the webpage isusing unicode and we cannot otherwise write to file (not an ascii string)
from email.mime.text import MIMEText
from pprint import pprint
# configure the  variable that is assigned to what is currently configured as OSX version in F5
#configuredReleaseNr = '10.11.3'
# save the variable into a json file as dict
#osxDict = {'confiuredReleaseNr': '10.11.3'}
#with open('osx.json', 'w') as output:
#     json.dump(osxDict, output)
dir_path = os.path.dirname(os.path.abspath(__file__))
json_data=open(os.path.join(dir_path, 'osx.json')).read()
with open(os.path.join(dir_path, 'osx.json')) as data_file:
     data = json.load(data_file)
pprint("Staticaly configured release value: "+str(data['confiuredReleaseNr']))
# downlod the OSX wiki page and create the BS4 types
page = requests.get('https://en.wikipedia.org/wiki/OS_X')
page.raise_for_status()
osxSoup = bs4.BeautifulSoup(page.text, "lxml")
########----------select the release version--------------------------------------------------
##############################################################################################
# the data is in the infobox and is an htmp "a" so bellow we seleect them all
tableCell = osxSoup.select('table.infobox.vevent a')
# the 22nd TD contains the latest value
html=tableCell[22]
# make this one string that looks like this
#<a href="/wiki/OS_X_El_Capitan" title="OS X El Capitan">10.11.3</a>
# a new BS4 object 
latestReleaseSoup =  bs4.BeautifulSoup(html.text, "lxml")
# select only the text not the hyperlink
latestReleaseNrSoup = latestReleaseSoup.findAll(text=True)
# print a number only format and no 'u.xxx
latestReleaseNr = ''.join(latestReleaseSoup.findAll(text=True))
########----------select the release date--------------------------------------------------
##############################################################################################
# select the  small element - there we have the release date
tableCellSmall = osxSoup.select('table.infobox.vevent small')
### get the text from the first item in the list - there is the x days ago - in fact there is just one item of this list
#####here we do all in one line (similar to the multi step process above)
daysAgo = ''.join( bs4.BeautifulSoup(tableCellSmall[0].text, "lxml").findAll(text=True))
### screen output if run from cli
print("Latest release nr: "+str(latestReleaseNr))
#print("Release date: "+daysAgo)
# if the value from infobox matches ours no action is needed just send a reassuring email
configuredReleaseNr = data['confiuredReleaseNr']
if latestReleaseNr == configuredReleaseNr:
	# convert latest releas nr to string so we can add to file
	latestReleaseNrStr = str(latestReleaseNr)
	print 'No change needed!'
	noChangeNeededFile = codecs.open(os.path.join(dir_path, 'noChangeNeeded.txt'), encoding='utf-8', mode= 'w+')
	noChangeNeededFile.write('No change needed : \n')
	noChangeNeededFile.write('The current release number is: ')
	noChangeNeededFile.write(latestReleaseNrStr)
	noChangeNeededFile.write('\n The staticaly configured release value is: ')
	noChangeNeededFile.write(configuredReleaseNr)
	noChangeNeededFile.write('\n Release date: ')
	noChangeNeededFile.write(daysAgo)
	noChangeNeededFile.close()
	fp = open(os.path.join(dir_path, 'noChangeNeeded.txt'), 'rb')
	msg = MIMEText(fp.read())
	fp.close()
	msg['From'] = 'carol.domokos@gmail.com'
	msg['To'] = 'carol.domokos@hpe.com'
	msg['Subject'] = 'OSX latest release'
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.ehlo()
 	smtpObj.starttls()
	smtpObj.login('carol.domokos@gmail.com','xxxxx')
	smtpObj.sendmail('carol.domokos@gmail.com', ['carol.domokos@hp.com'], msg.as_string())
	smtpObj.quit()
else:
#	releaseVariable = str(latestReleaseNr)
# write this variable to the json file overwriting the old value
# we will leave this to be manual	osxDict = {'confiuredReleaseNr': releaseVariable}
#	with open(str(os.getcwd())+'/osx.json', 'w') as output:
#		json.dump(osxDict, output)
	print 'Change needed!!!!!'
        # convert latest releas nr to string so we can add to file
        latestReleaseNrStr = str(latestReleaseNr)
        ChangeNeededFile = codecs.open(os.path.join(dir_path, 'ChangeNeeded.txt'), encoding='utf-8', mode= 'w+')
        ChangeNeededFile.write('A change is needed!!!!! \n')
        ChangeNeededFile.write('The current release number is: \n')
       	ChangeNeededFile.write(latestReleaseNrStr)
       	ChangeNeededFile.write('\n The staticaly configured release value is: ')
       	ChangeNeededFile.write(configuredReleaseNr)
       	ChangeNeededFile.write('\n Release date: ')
       	ChangeNeededFile.write(daysAgo)
       	ChangeNeededFile.close()
        fp = open(os.path.join(dir_path, 'ChangeNeeded.txt'), 'rb')
        msg = MIMEText(fp.read())
        fp.close()
       	msg['From'] = 'carol.domokos@gmail.com'
        msg['To'] = 'carol.domokos@hpe.com'
       	msg['Subject'] = 'OSX latest release - CHANGE NEEDED'
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
       	smtpObj.login('carol.domokos@gmail.com','xxxx')
        smtpObj.sendmail('carol.domokos@gmail.com', ['carol.domokos@hp.com'], msg.as_string())
       	smtpObj.quit()

