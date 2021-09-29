from ufc.route import find_main_event
from ufc import app
from ufc import route
from ufc import methods
from flask_sqlalchemy import SQLAlchemy
import threading
import time


def run_app():
    app.run(threaded=True)


if __name__ == '__main__':
    route.find_main_event()
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=methods.update)
    first_thread.start()
    time.sleep(10)
    second_thread.start()
