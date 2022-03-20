from typing import Tuple, List
from firebase_admin.db import Reference
from pandas import DataFrame
from modules.roles import Roles

from datetime import datetime


class Chat:
    """
    for managing the theater-chat
    """

    def __init__(self, messages_ref: Reference, roles: Roles) -> None:
        """
        requires a reference to the 'messages' node
        """
        self._reference = messages_ref
        self._roles = roles

    def add(self, role_id: str, text: str) -> None:
        if not self._roles.exists(id=role_id):
            raise ValueError(f'role with id {role_id} does not exist')

        self._reference.push({
            'roleID': role_id,
            'text': text,
            'timestamp': {
                '.sv': 'timestamp'
            }
        })

    def listen(self, callback) -> None:
        self._reference.listen(callback)

    def get(self) -> DataFrame:
        """
        """
        data = self._reference.order_by_child('timestamp').get()
        roles_list = self._roles.get()

        rows = []
        for id in data:
            rows.append({
                'id':
                id,
                'roleID':
                data[id]['roleID'],
                'roleName':
                next(role for role in roles_list
                     if role[0] == data[id]['roleID'])[1],
                'message':
                data[id]['text'],
                'timestamp':
                datetime.fromtimestamp(data[id]["timestamp"] / 1000)
            })

        return DataFrame(rows)
