import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from termcolor import colored
import time
from datetime import datetime

from modules.roles import Roles
from modules.chat import Chat
from modules.helpers import clear


def main() -> None:
    # fetch the service account key json file contents
    cred = credentials.Certificate('service-account-key.json')

    # initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(
        cred, {
            'databaseURL':
            'https://ghosts-of-data-past-default-rtdb.europe-west1.firebasedatabase.app/'
        })

    ref = db.reference('/')

    roles = Roles(ref.child('roles'))
    chat = Chat(ref.child('messages'), roles)

    # get all roles
    roles_list = roles.get()

    # show older messages?
    print('show old messages? (y/n)')
    if input('> ').lower() == 'y':
        show_from = 0
    else:
        show_from = int(
            datetime.now().timestamp() * 1000
        )  # get time in milliseconds dince unix epoch (server time format)

    # show timestamp?
    print('show timestamp? (y/n)')
    if input('> ').lower() == 'y':
        show_timestamp = True
    else:
        show_timestamp = False

    # clear terminal
    clear()

    # create a callback listener function to capture changes
    def listener(event):
        if event.data is not None:
            # workaround because data sometimes is a dict and other times a dict of dicts
            if 'roleID' in event.data:
                data = {'id': event.data}
            else:
                data = event.data

            for id in data:
                timestamp = datetime.fromtimestamp(data[id]["timestamp"] /
                                                   1000)
                date = timestamp.date()

                if date != listener.previous_date:
                    print(colored(date.strftime('%d %B %Y'), attrs=['bold']))
                    listener.previous_date = date

                if data[id]["timestamp"] > show_from:
                    role = next(role for role in roles_list
                                if role[0] == data[id]['roleID'])
                    print(
                        f'{role[1]} {timestamp.strftime("%H:%M:%S") if show_timestamp else ""}>',
                        colored(data[id]["text"], role[2]))

    listener.previous_date = None

    # watch the collection query
    chat.listen(listener)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    main()