###
# (C) Copyright [2019-2020] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

import unittest
import mock

from simplivity.connection import Connection
from simplivity import exceptions
from simplivity.resources import backups


class BackupTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.backups = backups.Backups(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(backups.URL)
        resource_data = [{'id': '12345'}, {'id': '67890'}]
        mock_get.return_value = {backups.DATA_FIELD: resource_data}

        backup_objs = self.backups.get_all()
        self.assertIsInstance(backup_objs[0], backups.Backup)
        self.assertEqual(backup_objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_found(self, mock_get):
        backup_name = "testname"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(backups.URL, backup_name)
        resource_data = [{'id': '12345', 'name': backup_name}]
        mock_get.return_value = {backups.DATA_FIELD: resource_data}

        backup_obj = self.backups.get_by_name(backup_name)
        self.assertIsInstance(backup_obj, backups.Backup)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_not_found(self, mock_get):
        backup_name = "testname"
        resource_data = []
        mock_get.return_value = {backups.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.backups.get_by_name(backup_name)

        self.assertEqual(error.exception.msg, "Resource not found with the name {}".format(backup_name))

    @mock.patch.object(Connection, "get")
    def test_get_by_id_found(self, mock_get):
        backup_id = "12345"
        url = "{}?case=sensitive&id={}&limit=500&offset=0&order=descending&sort=name".format(backups.URL, backup_id)
        resource_data = [{'id': backup_id}]
        mock_get.return_value = {backups.DATA_FIELD: resource_data}

        backup_obj = self.backups.get_by_id(backup_id)
        self.assertIsInstance(backup_obj, backups.Backup)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_id_not_found(self, mock_get):
        backup_id = "12345"
        resource_data = []
        mock_get.return_value = {backups.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.backups.get_by_id(backup_id)

        self.assertEqual(error.exception.msg, "Resource not found with the id {}".format(backup_id))

    def test_get_by_data(self):
        resource_data = {'id': '12345'}

        backup_obj = self.backups.get_by_data(resource_data)
        self.assertIsInstance(backup_obj, backups.Backup)
        self.assertEqual(backup_obj.data, resource_data)

    @mock.patch.object(Connection, "delete")
    def test_delete(self, mock_delete):
        mock_delete.return_value = None, [{'object_id': '12345'}]

        backup_data = {'name': 'name1', 'id': '12345'}
        backup = self.backups.get_by_data(backup_data)

        backup.delete()
        mock_delete.assert_called_once_with('/backups/12345', custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_delete_multiple_backups(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]

        backup_data = [{'name': 'name1', 'id': '12345'}]
        backups = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data["id"] for backup in backups]

        data = {"backup_id": backup_ids}

        self.backups.delete_multiple_backups(backups)

        mock_post.assert_called_once_with('/backups/delete', data, custom_headers=None)


if __name__ == '__main__':
    unittest.main()
