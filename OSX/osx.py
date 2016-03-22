#!/usr/bin/python
# load the modules to download http, parse it and to send emails
import requests, bs4
import smtplib
import json
import os
from email.mime.text import MIMEText
from pprint import pprint
# configure the  variable that is assigned to what is currently configured as OSX version in F5
#configuredReleaseNr = '10.11.3'
# save the variable into a json file as dict
#osxDict = {'confiuredReleaseNr': '10.11.3'}
#with open('osx.json', 'w') as output:
#     json.dump(osxDict, output)
json_data=open('/home/gufi/PYTHON_Learning/osx.json').read()
with open('/home/gufi/PYTHON_Learning/osx.json') as data_file:
     data = json.load(data_file)
pprint(data['confiuredReleaseNr'])
# downlod the OSX wiki page and create the BS4 types
page = requests.get('https://en.wikipedia.org/wiki/OS_X')
page.raise_for_status()
osxSoup = bs4.BeautifulSoup(page.text, "lxml")
# the data is in the infobox
tableCell = osxSoup.select('table.infobox.vevent a')
# the 22nd TD contains the latest value
html=tableCell[22]
# make this one string that looks like this
#<a href="/wiki/OS_X_El_Capitan" title="OS X El Capitan">10.11.3</a>
# a new BS4 object 
latestReleaseSoup =  bs4.BeautifulSoup(html.text, "lxml")
# select only the text not the hyperlynk
latestReleaseNrSoup = latestReleaseSoup.findAll(text=True)
# print a number only format and no 'u.xxx
latestReleaseNr = ''.join(latestReleaseSoup.findAll(text=True))
# if the value from infobox matches ours no action is needed just send a reassuring email
configuredReleaseNr = data['confiuredReleaseNr']
if latestReleaseNr == configuredReleaseNr:
	# convert latest releas nr to string so we can add to file
	latestReleaseNrStr = str(latestReleaseNr)
	print 'No change needed!'
	noChangeNeededFile = open('/home/gufi/PYTHON_Learning/noChangeNeeded.txt', 'w')
	noChangeNeededFile.write('No change needed current variable is:')
	noChangeNeededFile.write(latestReleaseNrStr)
	noChangeNeededFile.close()
	fp = open('/home/gufi/PYTHON_Learning/noChangeNeeded.txt', 'rb')
	msg = MIMEText(fp.read())
	fp.close()
	msg['From'] = 'carol.domokos@gmail.com'
	msg['To'] = 'carol.domokos@hpe.com;'
	msg['Subject'] = 'OSX latest release'
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.ehlo()
 	smtpObj.starttls()
	smtpObj.login('carol.domokos@gmail.com','password')
	smtpObj.sendmail('carol.domokos@gmail.com', ['carol.domokos@hp.com'], msg.as_string())
	smtpObj.quit()
else:
	releaseVariable = str(latestReleaseNr)
# write this variable to the json file overwriting the old value
	osxDict = {'confiuredReleaseNr': releaseVariable}
	with open(str(os.getcwd())+'/osx.json', 'w') as output:
		json.dump(osxDict, output)
		print 'Change needed!!!!!'
	        ChangeNeededFile = open('/home/gufi/PYTHON_Learning/ChangeNeeded.txt', 'w')
        	ChangeNeededFile.write('A change is needed, the current variable is: ')
	        ChangeNeededFile.write(releaseVariable)
        	ChangeNeededFile.close()
	        fp = open('/home/gufi/PYTHON_Learning/ChangeNeeded.txt', 'rb')
	        msg = MIMEText(fp.read())
	        fp.close()
        	msg['From'] = 'carol.domokos@gmail.com'
	        msg['To'] = 'carol.domokos@hpe.com;'
        	msg['Subject'] = 'OSX latest release'
	        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	        smtpObj.ehlo()
	        smtpObj.starttls()
        	smtpObj.login('carol.domokos@gmail.com','password')
	        smtpObj.sendmail('carol.domokos@gmail.com', ['carol.domokos@hp.com'], msg.as_string())
        	smtpObj.quit()

