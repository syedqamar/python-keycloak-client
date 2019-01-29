import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

__all__ = ('Users', 'User')


class Users(KeycloakAdminBase):
    _paths = {
        'collection': '/auth/admin/realms/{realm}/users'
    }

    _realm_name = None

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Users, self).__init__(*args, **kwargs)

    def create(self, username, **kwargs):
        """
        Create a user in Keycloak

        http://www.keycloak.org/docs-api/3.4/rest-api/index.html#_users_resource

        :param str username:
        :param object credentials: (optional)
        :param str first_name: (optional)
        :param str last_name: (optional)
        :param str email: (optional)
        :param boolean enabled: (optional)
        """
        payload = OrderedDict(username=username)

        if 'credentials' in kwargs:
            payload['credentials'] = [kwargs['credentials']]

        if 'first_name' in kwargs:
            payload['firstName'] = kwargs['first_name']

        if 'last_name' in kwargs:
            payload['lastName'] = kwargs['last_name']

        if 'email' in kwargs:
            payload['email'] = kwargs['email']

        if 'enabled' in kwargs:
            payload['enabled'] = kwargs['enabled']

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            data=json.dumps(payload),
            include_response_headers=True
        )

    def all(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            )
        )

    def by_id(self, id):
        return User(client=self._client, realm_name=self._realm_name, id=id)


class User(KeycloakAdminBase):
    _id = None
    _realm_name = None

    _paths = {
        'single': '/auth/admin/realms/{realm}/users/{id}',
        'totp': '/auth/realms/{realm}/account/totp?'
                'referrer=security-admin-console',
        'group_membership': '/auth/admin/realms/{realm}/users/{id}/groups',
        'membership_user_group': '/auth/admin/realms/{realm}/users/{'
                                 'id}/groups/{group_id}'
    }

    def __init__(self, realm_name, id, *args, **kwargs):
        self._id = id
        self._realm_name = realm_name
        super(User, self).__init__(*args, **kwargs)

    def update(self, name, **kwargs):
        payload = OrderedDict(name=name)

        for key in kwargs:
            payload[key] = kwargs[key]

        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('single',
                              realm=self._realm_name, id=self._id)
            ),
            data=json.dumps(payload)
        )

    def delete(self):
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path('single', id=self._id, realm=self._realm_name)
            )
        )

    def get_group_memberships(self, **kwargs):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('group_membership', id=self._id,
                              realm=self._realm_name), kwargs)
        )

    def join_group(self, group_id, **kwargs):
        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('membership_user_group', id=self._id,
                              realm=self._realm_name,
                              group_id=group_id), kwargs),
            data={}
        )

    def leave_group(self, group_id, **kwargs):
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path('membership_user_group', id=self._id,
                              realm=self._realm_name,
                              group_id=group_id), kwargs)
        )

    def configure_totp(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('totp', realm=self._realm_name)
            )
        )
