import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

GROUP_KWARGS = [
    'attributes',
    'realmRoles',
    'clientRoles',
    'subGroups',
    'access',
    'name'
]

__all__ = ('Groups', 'Group')


class Groups(KeycloakAdminBase):
    _paths = {
        'collection': '/auth/admin/realms/{realm}/groups'
    }

    _realm_name = None

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Groups, self).__init__(*args, **kwargs)

    def create(self, name, **kwargs):
        payload = OrderedDict(name=name)

        for key in GROUP_KWARGS:
            if key in kwargs:
                if key == 'attributes':
                    for k, v in kwargs.get('attributes').items():
                        kwargs['attributes'][k] = [str(v)]
                payload[key] = kwargs[key]

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
        return Group(client=self._client, realm_name=self._realm_name, id=id)


class Group(KeycloakAdminBase):
    _id = None
    _realm_name = None

    _paths = {
        'single': '/auth/admin/realms/{realm}/groups/{id}',
        'members': '/auth/admin/realms/{realm}/groups/{id}/members',
        'create_child': '/auth/admin/realms/{realm}/groups/{id}/children',
    }

    def __init__(self, realm_name, id, *args, **kwargs):
        self._id = id
        self._realm_name = realm_name
        super(Group, self).__init__(*args, **kwargs)

    def delete(self):
        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path('single', id=self._id, realm=self._realm_name)
            )
        )

    def create_child(self, name, **kwargs):
        payload = OrderedDict(name=name)

        for key in GROUP_KWARGS:
            if key in kwargs:
                if key == 'attributes':
                    for k, v in kwargs.get('attributes').items():
                        kwargs['attributes'][k] = [str(v)]
                payload[key] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('create_child', realm=self._realm_name,
                              id=self._id)
            ),
            data=json.dumps(payload),
            include_response_headers=True
        )

    def update(self, **kwargs):
        payload = OrderedDict()

        for key in GROUP_KWARGS:
            if key in kwargs:
                if key == 'attributes':
                    for k, v in kwargs.get('attributes').items():
                        kwargs['attributes'][k] = [str(v)]
                payload[key] = kwargs[key]

        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('single',
                              realm=self._realm_name, id=self._id)),
            data=json.dumps(payload)
        )

    def get_members(self, **kwargs):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('members',
                              realm=self._realm_name,
                              id=self._id),
                kwargs)
        )

    def get(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('single', realm=self._realm_name, id=self._id)
            )
        )
