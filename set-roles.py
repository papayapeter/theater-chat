"""for adding, editing & deleting roles that the chatters can perform"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from modules.roles import Roles


def main() -> None:
    # fetch the service account key json file contents
    cred = credentials.Certificate('service-account-key.json')

    # initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(
        cred, {
            'databaseURL':
            'https://ghosts-of-data-past-default-rtdb.europe-west1.firebasedatabase.app/'
        })

    roles = Roles(db.reference('/roles'))

    # main, keyboard interruptable loop
    try:
        while True:
            # allow user to add, remove or edit roles
            print(
                'would you like to [a]dd, [e]dit or [r]emove a role or [q]uit?'
            )
            reply = input('> ').lower()
            # add a role
            if reply == 'a':
                # name
                print('which role would you like to add?')
                name = input('> ').lower()

                # color
                print(
                    'which color should it have? (grey/red/green/yellow/blue/magenta/cyan/white)'
                )
                color = input('> ').lower()

                # confirmation
                print(f'add {name} with the color {color}? (y/n)')
                if input('> ').lower() == 'y':
                    roles.add(name, color)

            # edit a role
            elif reply == 'e':
                # which role
                print('which role would you like to edit?')

                # list all roles
                roles_list = roles.get()
                for index, role in enumerate(roles_list):
                    print(f'{index}: {role[1]}')

                # change
                index = int(input('> '))
                if index < len(roles_list):
                    name = input(
                        f'name: original: {roles_list[index][1]} | new (keep blank to keep original)> '
                    ).lower()
                    color = input(
                        f'color: original: {roles_list[index][2]} | new (keep blank to keep original)> '
                    )
                    roles.edit(roles_list[index][0], name, color)
                else:
                    print('out of range!')

            # remove a role
            elif reply == 'r':
                # which role
                print('which role would you like to remove?')

                # list all roles
                roles_list = roles.get()
                for index, role in enumerate(roles_list):
                    print(f'{index}: {role[1]}')

                # delete
                index = int(input('> '))
                if index < len(roles_list):
                    roles.delete(roles_list[index][0])
                else:
                    print('out of range!')

            # quit
            elif reply == 'q':
                return

            else:
                print('wrong input!')
    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    main()