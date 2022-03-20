from cgitb import reset
from typing import Tuple, List
from unittest import result
from firebase_admin.db import Reference

POSSIBLE_COLORS = [
    'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
]


class Roles:
    """
    for managing all roles for the theater-chat
    """

    def __init__(self, roles_ref: Reference) -> None:
        """
        requires a reference to the 'roles' node
        """
        self._reference = roles_ref

    def get(self,
            id: str = None,
            name: str = None,
            color: str = None) -> List[Tuple[str, str, str]]:
        """
        gets all matches to an id, name or color.

        if no argument is set, all roles are returned
        if more than one argument is set, the latter ones will be ignored.

        returns as a list of tuples: [(id, name, color), ...]
        """
        # if getting by id
        if id:
            ref = self._reference.order_by_key().equal_to(id)
        # if getting by name
        elif name:
            ref = self._reference.order_by_child('name').equal_to(name)
        # if getting by color
        elif color:
            ref = self._reference.order_by_child('color').equal_to(color)
        # get all
        else:
            ref = self._reference.order_by_key()

        snapshot = ref.get()

        return [(key, val['name'], val['color'])
                for key, val in snapshot.items()]

    def get_id(self, name: str = None, color: str = None) -> str:
        """
        gets the first id that matches the name and/or color.
        """

        result = self.get(name=name, color=color)
        if not len(result):
            return None
        else:
            return result[0][0]

    def exists(self,
               id: str = None,
               name: str = None,
               color: str = None) -> bool:
        return bool(self.get(id, name, color))

    def edit(self,
             id: str,
             new_name: str = None,
             new_color: str = None) -> None:
        # assemble the changes
        update_dict = {}
        if new_name:
            # check if user with this name already exists
            if self.exists(name=new_name):
                raise ValueError(
                    f'user with the name {new_name} already exists')

            update_dict['name'] = new_name

        if new_color:
            # check if the color is possible
            if new_color not in POSSIBLE_COLORS:
                raise ValueError(f'color must be one of {POSSIBLE_COLORS}')

            update_dict['color'] = new_color

        # update the role
        self._reference.child(id).update(update_dict)

    def add(self, name: str, color: str) -> None:
        # check if user with this name already exists
        if self.exists(name=name):
            raise ValueError(f'user with the name {name} already exists')

        # check if the color is possible
        if color not in POSSIBLE_COLORS:
            raise ValueError(f'color must be one of {POSSIBLE_COLORS}')

        self._reference.push({'name': name, 'color': color})

    def delete(self, id: str) -> None:
        self._reference.child(id).delete()
