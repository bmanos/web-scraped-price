# Web scraping mymarket prices to
# get email alerts about price changes
# Author        : Bairaktaris Emmanuel
# Date          : December 6, 2019
# Last modified : March 15, 2020
# Link  : http://repairmypc.net

# Import librairies
import requests
from bs4 import BeautifulSoup
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
    message['Subject'] = 'New price for item ' + mypricestitle
    body = 'The new price is : ' + mypricesprice +'\nThe previous prices was : ' + content_file +'\nThe product link  is : ' + myurls
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

mylinks = ['https://eshop.mymarket.gr/proino-rofimata-kafes/kafes/espresso-capuccino/lavazza-kafes-espresso-oro-250gr',\
           'https://eshop.mymarket.gr/proino-rofimata-kafes/eidi-epaleipsis/pralina/merenda-230gr',\
           'https://eshop.mymarket.gr/oikiaki-frontida-chartika/katharistika-spitiou/genikis-chrisis/dettol-apolymantiko-spray-epifaneion']

# Get the links to be scraped
for myurls in mylinks:
    r = requests.get(myurls)
    soup = BeautifulSoup(r.text, 'html.parser')
    refresh = soup.find_all('meta', attrs={'http-equiv': 'Pragma', 'content': 'no-cache'})
    refresh = soup.find_all('meta', attrs={'http-equiv': 'Expires', 'content': '-1'})
    refresh = soup.find_all('meta', attrs={'http-equiv': 'cache-control', 'content': 'NO-CACHE'})
    time.sleep(10)

    myprices = requests.get(myurls)

    soup_myprices = BeautifulSoup(myprices.text, 'html.parser')

    # Extract text of Product title
    mypricestitle = soup_myprices.find(class_='page-title').get_text()
    print(mypricestitle)

    # Extract text of Product code
    mypricescode = soup_myprices.find(class_='facebook-pixel-sku').get_text()
    print(mypricescode)

    # Extract text of price
    mypricesprice = soup_myprices.find(class_='price final-price').get_text()
    print(mypricesprice)
    print(myurls)

    #filepath = '/home/pi/scripts/myprices-'+ mypricestitle + '.txt'
    filepath = '/Users/manos/Documents/Projects/python-projects/myprices-'+ mypricescode + '.txt'

    # Check if file exist and if it doesn't create the file
    #file = open('/home/pi/scripts/myprices-'+ mypricestitle + '.txt','a')
    file = open('/Users/manos/Documents/Projects/python-projects/myprices-'+ mypricescode + '.txt','a')
    file.close()

    # Open files
    with open(filepath, 'r') as f:
        # Get all the contents of the file
        content_file = f.read()

        # Remove any whitespace at the end
        content_file = content_file.strip()

        # Compare with the price
        user_input = mypricesprice
        
    if user_input == content_file:
        print('No price changed')
    else:
        print('Price changed. Sending email...')
        sendEmail()

    # Write the price to the file so you could compare it next time
    #file = open('/home/pi/scripts/myprices-'+ mypricestitle + '.txt','w')
    file = open('/Users/manos/Documents/Projects/python-projects/myprices-'+ mypricescode + '.txt','w')
    file.write(mypricesprice)
    file.close()
