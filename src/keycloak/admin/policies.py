import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

POLICY_TYPES = {
    'role'
}


class Policies(KeycloakAdminBase):
    _paths = {
        'collection': '/auth/admin/realms/{realm}/clients/{'
                      'client_id}/authz/resource-server/policy?permission'
                      '=false',
        'create': '/auth/admin/realms/{realm}/clients/{'
                  'client_id}/authz/resource-server/policy/role'
    }

    _realm_name = None

    def __init__(self, realm_name, client_id, *args, **kwargs):
        self._realm_name = realm_name
        self._client_id = client_id
        super(Policies, self).__init__(*args, **kwargs)

    def create(self, name, **kwargs):
        payload = OrderedDict(name=name)

        for key in kwargs:
            payload[key] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('create', realm=self._realm_name,
                              client_id=self._client_id)
            ),
            data=json.dumps(payload)
        )

    def all(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name,
                              client_id=self._client_id)
            )
        )


class RolePolicy(KeycloakAdminBase):
    _paths = {
        'create_with_role': '/auth/admin/realms/{realm}/clients/{'
                            'client_id}/authz/resource-server/policy/role'
    }

    def __init__(self, realm_name, client_id, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name

        super(RolePolicy, self).__init__(*args, **kwargs)
