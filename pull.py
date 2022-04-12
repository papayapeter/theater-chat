"""for exporting all chat data from the firebase realtimedatabase to json"""

from email import message
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from termcolor import colored
from datetime import datetime
import json

from modules.roles import Roles
from modules.chat import Chat


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

    # get all messages and dump them into a json file
    with open('chat_data.json', 'w+', encoding='utf8') as file:
        json.dump(chat.get(), file, indent=4, default=str, ensure_ascii=False)

    # get all messages from json file and print them out
    with open('chat_data.json', encoding='utf8') as file:
        chat_data = json.load(file)

    print(f'message count: {len(chat_data)}')


if __name__ == '__main__':
    main()