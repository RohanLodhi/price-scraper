from datetime import datetime
import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = input("Please enter the product's URL: ")
userAgent = input("Please enter your device's user agent (can be found by googling 'my user agent'): ")
wish_price = input("Please enter the price at which you want to get notified: ")
mailId = input("Please enter your email address where you want the email to be sent: ")
interval = int(input("Please enter the interval of seconds after which you want to check the price: "))
headers = {"User-Agent": userAgent}

page = requests.get(URL, headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')
soup2 = BeautifulSoup(soup.prettify(), 'html.parser')
title = soup2.find(id="title").get_text().strip()
price = soup2.find(id="priceblock_ourprice").get_text()
price = price.strip()
print(price)
price = price.replace(",","")
converted_price = price[2:]

def send_mail(id, title):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('noreply.pricebot@gmail.com', password='lqnkqvsvgfhotaza')

    TO = mailId
    subject = 'Price drop noticed!'
    body = 'A price drop has been detected by our systems on the requested product ' + title

    msg = "Subject: {}\n\n{}".format(subject,body) 

    server.sendmail(
        'noreply.pricebot@gmail.com',
        TO,
        msg
    )

    server.quit()

def check_status(interval):
    if converted_price <= wish_price:
        send_mail(mailId, title)
        print("Email has been sent")
        print("Product value is ", converted_price)
        exit()

    else:
        print(datetime.now())
        print("We are sorry, Price did not drop. Price is ", converted_price)

while True:
    check_status(interval)
    time.sleep(interval)
