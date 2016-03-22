#!/usr/bin/python
### credit answer of J.F Sebastian
##### http://stackoverflow.com/questions/613471/discovering-public-ip-programatically
import dns.resolver # $ pip install dnspython
import smtplib
import json
import datetime
from email.mime.text import MIMEText
from pprint import pprint
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ["208.67.222.222", "208.67.220.220"]
myIp=(resolver.query('myip.opendns.com')[0])
today = datetime.date.today()
now = datetime.datetime.now()
ipDict = {'date':str(today),'time':str(now),'addr':str(myIp)}
with open('/home/gufi/PYTHON_Learning/dyDNS.json') as data_file:
     data = json.load(data_file)
     lastIp = data [-1]
     print('Last IP address'+ lastIp['addr'])
     print (myIp)
     if str(lastIp['addr']) != str(myIp):
         ipHist = data + [ipDict]
         print('IP address has changed')
	 with open('/home/gufi/PYTHON_Learning/dyDNS.json', 'w') as output:
	     json.dump(ipHist, output)
	 ipAddrFile = open('ipAddressMail.txt', 'w')
	 ipAddrFile.write('The current IP is: '+str(lastIp['addr'])+"\n")
	 ipAddrFile.write('The list of IPs and their install dates \n')
	 ipAddrFile.write('Date:     ')
	 ipAddrFile.write("IP ADDRESS:     \n")
	 ipAddrFile.write(str(lastIp['date']))
	 ipAddrFile.write(str(lastIp['addr']))
	 ipAddrFile.close()
	 fp = open('ipAddressMail.txt', 'rb')
	 msg = MIMEText(fp.read())
	 fp.close()
	 msg['From'] = 'carol.domokos@gmail.com'
	 msg['To'] = 'carol.domokos@hpe.com'
	 msg['Subject'] = 'Rizolli IP address'
	 smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	 smtpObj.ehlo()
	 smtpObj.starttls()
	 smtpObj.login('carol.domokos@gmail.com','password')
	 smtpObj.sendmail('carol.domokos@gmail.com', ['carol.domokos@hp.com'], msg.as_string())
	 smtpObj.quit()
     else:
	  print('No change in IP address')
