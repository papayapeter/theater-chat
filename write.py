"""for writing into the chat"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import readline

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

    try:
        roles_list = roles.get()
        if not len(roles_list):
            print('no roles set!')
            return

        # which role
        print('which role will you perform?')

        # list all roles
        for index, role in enumerate(roles_list):
            print(f'{index}: {role[1]}')

        # pick role
        index = int(input('> '))
        if index < len(roles_list):
            # get an list original data
            role = roles_list[index]

        # main loop
        while True:
            clear()
            message = input('> ')
            chat.add(role[0], message)

    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    main()