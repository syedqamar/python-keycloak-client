import json
from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.realm import KeycloakRealm


class KeycloakAdminRoleMappingsTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token('some-token')

    def test_details_group(self):
        self.admin.realms.by_name('realm-name').clients.by_id(
            '#123').role_mappings.by_group('group1').details()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups/group1/'
            'role-mappings/clients/#123'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_create_group(self):
        roles = [{'id': '123'}]
        self.admin.realms.by_name('realm-name').clients.by_id(
            '#123').role_mappings.by_group('group1').create(
            roles=roles
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups/group1/'
            'role-mappings/clients/#123'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data=json.dumps(roles),
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_delete_group(self):
        roles = [{'id': '123'}]
        self.admin.realms.by_name('realm-name').clients.by_id(
            '#123').role_mappings.by_group('group1').delete(
            roles=roles
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups/group1/'
            'role-mappings/clients/#123'
        )
        self.realm.client.delete.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data=json.dumps(roles),
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_details_user(self):
        self.admin.realms.by_name('realm-name').clients.by_id(
            '#123').role_mappings.by_user('user1').details()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/users/user1/'
            'role-mappings/clients/#123'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
