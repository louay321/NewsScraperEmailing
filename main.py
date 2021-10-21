# This project is a news scraper using beautiful soup that will send Top news from a news website
# (depending on context) and send it through e-mail


# import the libraries to use
import requests
# Handles Http requests
import datetime
# will send the exact time of the extracted news
import smtplib
# Sending the email through SMTP protocol
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# these two mime library functions will create the email body
from bs4 import BeautifulSoup
# web scraping using beautifulsoup

# extracting the content

def extract_content(url):
    cont = ""
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    #extract all the data within html 'td' tag with class of 'title' (depending on website structure)
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cont += ((str(i+1)+ ' -: ' + tag.text + '\n') if tag.text != 'More' else '')
    return (cont)
content = ''
cont = extract_content('https://news.ycombinator.com/')
content += cont

# print(content)

# Sending the email with the content as body
SERVER = 'smtp.gmail.com'
PORT = 595
FROM =  ''
TO = ''
PASS = '*'

now = datetime.datetime.now()
msg = MIMEMultipart()
msg['Subject'] = 'HackerNews top stories' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))


print('Starting to send..')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Sent successfully!')

server.quit()

