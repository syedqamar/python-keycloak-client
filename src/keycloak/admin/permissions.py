import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase

POLICY_TYPES = {
    'role'
}


class Permissions(KeycloakAdminBase):
    _paths = {
        'collection': '/auth/admin/realms/{realm}/clients/{'
                      'client_id}/authz/resource-server/permission'
    }

    _realm_name = None

    def __init__(self, realm_name, client_id, *args, **kwargs):
        self._realm_name = realm_name
        self._client_id = client_id
        super(Permissions, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name,
                              client_id=self._client_id)
            )
        )

    def by_id(self, permission_id):
        return Permission(realm_name=self._realm_name,
                          client_id=self._client_id,
                          permission_id=permission_id, client=self._client)


class Permission(KeycloakAdminBase):
    _paths = {
        'single': '/auth/admin/realms/{realm}/clients/{'
                  'client_id}/authz/resource-server/permission/scope/{'
                  'permission_id}',
        'associated_policies': '/auth/admin/realms/{realm}/clients/{'
                               'client_id}/authz/resource-server/policy/{'
                               'permission_id}/associatedPolicies',
        'scopes': '/auth/admin/realms/{realm}/clients/{'
                  'client_id}/authz/resource-server/policy/{'
                  'permission_id}/scopes',
        'resources': '/auth/admin/realms/{realm}/clients/{'
                     'client_id}/authz/resource-server/policy/{'
                     'permission_id}/resources'
    }

    def __init__(self, realm_name, client_id, permission_id, *args, **kwargs):
        self._client_id = client_id
        self._realm_name = realm_name
        self._permission_id = permission_id

        super(Permission, self).__init__(*args, **kwargs)

    def get(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('single', realm=self._realm_name,
                              permission_id=self._permission_id,
                              client_id=self._client_id)
            )
        )

    def get_associated_policies(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('associated_policies', realm=self._realm_name,
                              permission_id=self._permission_id,
                              client_id=self._client_id)
            )
        )

    def get_associated_scopes(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('scopes', realm=self._realm_name,
                              permission_id=self._permission_id,
                              client_id=self._client_id)
            )
        )

    def get_associated_resources(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('resources', realm=self._realm_name,
                              permission_id=self._permission_id,
                              client_id=self._client_id)
            )
        )

    def update(self, name, **kwargs):
        payload = OrderedDict(name=name)

        for key in kwargs:
            payload[key] = kwargs[key]

        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('single',
                              realm=self._realm_name,
                              client_id=self._client_id,
                              permission_id=self._permission_id)),
            data=json.dumps(payload)
        )
