import time
from datetime import datetime, date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ufc.model import Record
from bs4 import BeautifulSoup
import requests
from ufc import db


def getFight1():
    html_text = requests.get('https://www.espn.com/mma/fightcenter').text
    soup = BeautifulSoup(html_text, 'lxml')
    fights = soup.find_all(
        'div', class_='MMACompetitor__Detail flex flex-column justify-center')
    i = 0
    arr = [None] * 2
    for fight in fights:
        if i < 2:
            fighter_name = fight.h2.span.text
            arr[i] = fighter_name
            i = i + 1
    return arr


def update():
    event_start_time = input('Enter time of main event: ')
    x = date.today()
    today = x.strftime("%B %d, %Y")
    y = datetime.now()
    now = y.strftime("%H:%M")

    hour, minute = now.split(':')
    current_time = int(hour) * 60 + int(minute)

    h, m = event_start_time.split(':')
    fight_time = ((int(h) + 12) * 60) + (int(m) + 6)  # covert to minutes

    print(f"Today's Date: {today}")
    print(f"Current time: {now}")
    print(f"Fight time: {event_start_time}")

    while True:
        users = Record.query.filter_by(fight_date=today).all()
        # There is a fight today so time.sleep for less time
        if len(users) != 0:
            # The current time is past the time of the main event
            if (fight_time <= current_time):
                # update website and check against the value of fight1
                fightOne = getFight1()

                for i in users:
                    if i.fight in fightOne[0]:
                        email(i.email, fightOne)
                        print(f'Email sent!')
                        Record.query.filter_by(fight=i.fight).delete()
                        db.session.commit()
                print(f'Waiting 5 minutes...')
                time.sleep(5*60)
            else:
                print(f'Waiting 30 minutes...')
                time.sleep(30*60)
        # There is no fight today
        else:
            getFight1()
            print(f'Waiting 6 hours...')
            time.sleep(6*3600)


def email(user_emails, fightOne):
    # Email Account
    email_sender_account = "UFC Fight Alert"
    email_sender_username = "sirdevbot007@gmail.com"
    # REMINDER!!!!: MAKE THIS AN INPUT
    email_sender_password = "python4evah$"
    email_smtp_server = "smtp.gmail.com"
    email_smtp_port = 587

    # Email Account
    email_recepients = user_emails  # ["samueljryan98@gmail.com"]
    email_subject = "Fight is Starting"
    email_body = f"{fightOne[0]} vs. {fightOne[1]} is coming next!"

    # login to email server
    server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    server.starttls()
    server.login(email_sender_username, email_sender_password)

    # For loop, sending emails to all email recepients

    print(f"Sending email to {email_recepients}")
    message = MIMEMultipart('alternative')
    message['From'] = email_sender_account
    message['To'] = email_recepients
    message['Subject'] = email_subject
    message.attach(MIMEText(email_body, 'html'))
    text = message.as_string()
    server.sendmail(email_sender_username, email_recepients, text)

    # All email sent, log out
    server.quit()
