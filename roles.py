import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def main() -> None:
    # initialize database
    cred = credentials.Certificate('service-account-key.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

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
                    db.collection('roles').document(name).set({
                        'name': name,
                        'color': color
                    })

            # edit a role
            elif reply == 'e':
                # which role
                print('which role would you like to edit?')

                # list all roles
                roles = db.collection('roles').get()
                for index, role in enumerate(roles):
                    print(f'{index}: {role.to_dict()["name"]}')

                # change
                index = int(input('> '))
                if index < len(roles):
                    # get an list original data
                    data = roles[index].to_dict()
                    name = input(
                        f'name: original: {data["name"]} | new (keep blank to keep original)> '
                    ).lower()
                    if not name:
                        name = data['name']
                    color = input(
                        f'color: original: {data["color"]} | new (keep blank to keep original)> '
                    )
                    if not color:
                        color = data['color']
                    db.collection('roles').document(roles[index].id).set({
                        'name':
                        name,
                        'color':
                        color
                    })
                else:
                    print('out of range!')

            # remove a role
            elif reply == 'r':
                # which role
                print('which role would you like to remove?')

                # list all roles
                roles = db.collection('roles').get()
                for index, role in enumerate(roles):
                    print(f'{index}: {role.to_dict()["name"]}')

                # delete
                index = int(input('> '))
                if index < len(roles):
                    db.collection('roles').document(roles[index].id).delete()
                else:
                    print('out of range!')

            # quit
            elif reply == 'q':
                return

            else:
                print('wrong input!')
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()