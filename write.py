from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from helpers import clear


def main() -> None:
    # initialize database
    cred = credentials.Certificate('service-account-key.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    try:
        roles = db.collection('roles').get()
        if not len(roles):
            print('no roles set!')
            return

        # which role
        print('which role will you perform?')

        # list all roles
        for index, role in enumerate(roles):
            print(f'{index}: {role.to_dict()["name"]}')

        # pick role
        index = int(input('> '))
        if index < len(roles):
            # get an list original data
            role = roles[index]

        # main loop
        while True:
            clear()
            message = input('> ')
            now = datetime.now()
            db.collection('chat').add({
                'roleID': role.id,
                'message': message,
                'timestamp': now
            })

    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()