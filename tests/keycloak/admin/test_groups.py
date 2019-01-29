from unittest import TestCase

import mock

from keycloak.admin import KeycloakAdmin
from keycloak.realm import KeycloakRealm


class KeycloakAdminGroupsTestCase(TestCase):

    def setUp(self):
        self.realm = mock.MagicMock(spec_set=KeycloakRealm)
        self.admin = KeycloakAdmin(realm=self.realm)
        self.admin.set_token('some-token')

    def test_create(self):
        self.admin.realms.by_name('realm-name').groups.create(
            name='group-name'
        )
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups'
        )
        self.realm.client.post.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            data='{"name": "group-name"}',
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_all(self):
        self.admin.realms.by_name('realm-name').groups.all()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups'
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_delete(self):
        self.admin.realms.by_name('realm-name').groups.by_id('abc').delete()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups/abc'
        )
        self.realm.client.delete.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_members(self, **kwargs):
        self.admin.realms.by_name('realm-name').\
            groups.by_id('abc').get_members()
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups/abc/members', kwargs
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )

    def test_get_members_with_query_params(self, **kwargs):
        kwargs['max'] = 20
        self.admin.realms.by_name('realm-name').\
            groups.by_id('abc').get_members(**kwargs)
        self.realm.client.get_full_url.assert_called_once_with(
            '/auth/admin/realms/realm-name/groups/abc/members', kwargs
        )
        self.realm.client.get.assert_called_once_with(
            url=self.realm.client.get_full_url.return_value,
            headers={
                'Authorization': 'Bearer some-token',
                'Content-Type': 'application/json'
            }
        )
