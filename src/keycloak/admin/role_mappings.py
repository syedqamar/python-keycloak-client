import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

__all__ = ('RoleMappings', 'GroupRoleMappings', 'UserRoleMappings',)


class RoleMappings(KeycloakAdminBase):
    _client_id = None
    _realm_name = None

    def __init__(self, realm_name, client_id, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name
        super(RoleMappings, self).__init__(*args, **kwargs)

    def by_group(self, group_id):
        return GroupRoleMappings(realm_name=self._realm_name,
                                 client_id=self._client_id,
                                 group_id=group_id, client=self._client)

    def by_user(self, user_id):
        return UserRoleMappings(realm_name=self._realm_name,
                                client_id=self._client_id,
                                user_id=user_id, client=self._client)


class GroupRoleMappings(KeycloakAdminBase):
    _paths = {
        'group_mappings_client': '/auth/admin/realms/{realm}/groups/{group_id}'
                                 '/role-mappings/clients/{id}'
    }

    def __init__(self, realm_name, client_id, group_id, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name
        self._group_id = group_id

        super(GroupRoleMappings, self).__init__(*args, **kwargs)

    def details(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('group_mappings_client', realm=self._realm_name,
                              id=self._client_id, group_id=self._group_id)
            )
        )

    def create(self, roles):
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('group_mappings_client',
                              realm=self._realm_name, id=self._client_id,
                              group_id=self._group_id)
            ),
            data=json.dumps(roles)
        )

    def delete(self, roles):
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path('group_mappings_client',
                              realm=self._realm_name, id=self._client_id,
                              group_id=self._group_id)
            ),
            data=json.dumps(roles)
        )


class UserRoleMappings(KeycloakAdminBase):
    _paths = {
        'user_mappings_client': '/auth/admin/realms/{realm}/users/{user_id}'
                                '/role-mappings/clients/{id}'
    }

    def __init__(self, realm_name, client_id, user_id, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name
        self._user_id = user_id

        super(UserRoleMappings, self).__init__(*args, **kwargs)

    def details(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('user_mappings_client', realm=self._realm_name,
                              id=self._client_id, user_id=self._user_id)
            )
        )

    def create(self, roles):
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('user_mappings_client',
                              realm=self._realm_name, id=self._client_id,
                              user_id=self._user_id)
            ),
            data=json.dumps(roles)
        )

    def delete(self, roles):
        payload = OrderedDict(roles=roles)

        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path('user_mappings_client',
                              realm=self._realm_name, id=self._client_id,
                              user_id=self._user_id)
            ),
            data=json.dumps(payload)
        )
