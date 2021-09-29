
from ufc.model import Record
from flask import flash, render_template, request
from ufc.model import Record
from ufc import app, db
from bs4 import BeautifulSoup
import requests


event_start_time = ''
event_name = ''
event_date = ''
fight1 = ''
fight2 = ''
fight3 = ''
fight4 = ''
fight5 = ''


# web scrapes necessary information
def find_main_event():
    global event_start_time, event_name, event_date, fight1, fight2, fight3, fight4, fight5
    html_text = requests.get('https://www.espn.com/mma/fightcenter').text
    soup = BeautifulSoup(html_text, 'lxml')
    event = soup.find('div', class_='flex flex-column pt5 pr5')
    fights = soup.find_all(
        'div', class_='MMACompetitor__Detail flex flex-column justify-center')

    event_date = soup.find('div', class_='n6 mb2').text

    event_name = event.h1.text
    i = 0
    arr = [None] * 10
    for fight in fights:
        if i < 10:
            fighter_name = fight.h2.span.text
            arr[i] = fighter_name
            i = i + 1

    fight1 = (f"{arr[0]} vs. {arr[1]}")
    fight2 = (f"{arr[2]} vs. {arr[3]}")
    fight3 = (f"{arr[4]} vs. {arr[5]}")
    fight4 = (f"{arr[6]} vs. {arr[7]}")
    fight5 = (f"{arr[8]} vs. {arr[9]}")

    # home(event_start_time, event_name, event_date,
    #    fight1, fight2, fight3, fight4, fight5)


# displays information
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        email = request.form.get('email')
        fight = request.form.get('fight')
        record = Record(email=email,
                        fight=fight, fight_date=event_date)
        db.session.add(record)
        db.session.commit()
        flash(f'Alert has been created!', 'success')
        print("success!")
    print(f'{event_start_time} eastern')

    return render_template('home.html', event_name=event_name, date=event_date, event_start_time=event_start_time,
                           fight1=fight1, fight2=fight2, fight3=fight3, fight4=fight4, fight5=fight5)
