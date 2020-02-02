# Web scraping mymarket price to
# get email alert about price change
# Author        : Bairaktaris Emmanuel
# Date          : December 6, 2019
# Last modified : January 5, 2020
# Link  : http://repairmypc.net

# Import libraries
import requests
from bs4 import BeautifulSoup
import uuid
import datetime
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  
# Function to send email
def sendEmail():
    fromrecipient = 'm@m.gr'
    torecipient = 'm@m.gr'
    bcc = 'mm@m.gr'
    message = MIMEMultipart()
    message['From'] = fromrecipient
    message['To'] = torecipient
    message['Subject'] = 'New price for my prefered coffee'
    body = 'The new price for my coffee is : ' + coffeeprice +'\nThe previous price was : ' + content_file +'\nThe product link  is : https://eshop.mymarket.gr/proino-rofimata-kafes/kafes/espresso-capuccino/lavazza-kafes-espresso-oro-250gr'
    message.attach(MIMEText(body, 'plain'))

    import smtplib
    server = smtplib.SMTP('mail.server.gr:587')
    server.starttls()
    server.ehlo()

    server.login('ma@.gr', 'mysupersecurepassword')

    text = message.as_string()
    #server.sendmail(fromrecipient, torecipient, text)
    server.sendmail(message['From'], [torecipient, bcc], text)
    return

# Get yesterday date
today = datetime.date.today()
mydate = today - datetime.timedelta(days = 1)

# Get the links to be scraped Coffee
r = requests.get('https://eshop.mymarket.gr/proino-rofimata-kafes/kafes/espresso-capuccino/lavazza-kafes-espresso-oro-250gr')
soup = BeautifulSoup(r.text, 'html.parser')
refresh = soup.find_all('meta', attrs={'http-equiv': 'Pragma', 'content': 'no-cache'})
refresh = soup.find_all('meta', attrs={'http-equiv': 'Expires', 'content': '-1'})
refresh = soup.find_all('meta', attrs={'http-equiv': 'cache-control', 'content': 'NO-CACHE'})
time.sleep(10)

coffee = requests.get('https://eshop.mymarket.gr/proino-rofimata-kafes/kafes/espresso-capuccino/lavazza-kafes-espresso-oro-250gr')

soup_coffee = BeautifulSoup(coffee.text, 'html.parser')

# Extraxt text of currency price
coffeeprice = soup_coffee.find(class_='price final-price').get_text()
print(coffeeprice)

#filepath = '/home/pi/scripts/coffee.txt'
filepath = '/Users/manos/Documents/Projects/python-projects/coffee.txt'

# Open files
with open(filepath, 'r') as f:
    # Get all the contents of the file
    content_file = f.read()

    # Remove any whitespace at the end, e.g. a newline
    content_file = content_file.strip()

    # Compare with the ip get by the function
    user_input = coffeeprice
    
if user_input == content_file:
    print('No price changed')
else:
    print('Price changed. Sending email...')
    sendEmail()

# Write the price to the file so you could compare it next time
#file = open('/home/pi/scripts/coffee.txt','w')
file = open('/Users/manos/Documents/Projects/python-projects/coffee.txt','w')
file.write(coffeeprice)
file.close()