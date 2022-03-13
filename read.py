import time
import sys
# import threading
from datetime import datetime
from termcolor import colored
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from helpers import clear


def main() -> None:
    # initialize database
    cred = credentials.Certificate('service-account-key.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    # # create an event for notifying main thread
    # change_detected = threading.Event()

    # clear terminal
    clear()

    # get all roles
    roles = db.collection('roles').get()
    roles_dict = {}
    for role in roles:
        roles_dict[role.id] = role.to_dict()

    # create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                data = change.document.to_dict()
                print(
                    colored(f'{data["roleID"]}> {data["message"]}',
                            roles_dict[data['roleID']]['color']))

        # change_detected.set()

    now = datetime.now()

    # show older messages?
    print(f'show old messages? (y/n)')
    if input('> ').lower() == 'y':
        col_query = db.collection('chat')
    else:
        col_query = db.collection('chat').where('timestamp', '>', now)

    # watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()