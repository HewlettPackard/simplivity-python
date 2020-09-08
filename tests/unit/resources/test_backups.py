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
from unittest import mock
from unittest.mock import call

from simplivity.connection import Connection
from simplivity import exceptions
from simplivity.resources import backups
from simplivity.resources import datastores
from simplivity.resources import virtual_machines
from simplivity.resources import omnistack_clusters
from simplivity.resources import cluster_groups


class BackupTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.backups = backups.Backups(self.connection)
        self.datastores = datastores.Datastores(self.connection)
        self.virtual_machines = virtual_machines.VirtualMachines(self.connection)
        self.clusters = omnistack_clusters.OmnistackClusters(self.connection)
        self.cluster_groups = cluster_groups.ClusterGroups(self.connection)

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

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_restore_original_true(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = {'name': 'name1', 'id': '12345'}
        vm_data = [{'id': '12345', 'name': 'vm1'}]
        mock_get.return_value = {virtual_machines.DATA_FIELD: [vm_data]}
        backup = self.backups.get_by_data(backup_data)

        vm = backup.restore(True)
        self.assertIsInstance(vm, virtual_machines.VirtualMachine)

        mock_post.assert_called_once_with('/backups/12345/restore?restore_original=True', {}, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_restore_original_datastore_name(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        datastore_data = {'id': 'abcdef', 'name': 'ds1'}
        vm_data = [{'id': '12345', 'name': 'vm1'}]
        mock_get.side_effect = [{datastores.DATA_FIELD: [datastore_data]}, {virtual_machines.DATA_FIELD: [vm_data]}]
        backup_data = {'name': 'name1', 'id': '12345'}
        backup = self.backups.get_by_data(backup_data)
        vm = backup.restore(False, "vm1", "ds1")
        self.assertIsInstance(vm, virtual_machines.VirtualMachine)
        self.assertEqual(vm.data, vm_data)
        data = {'virtual_machine_name': 'vm1', 'datastore_id': 'abcdef'}
        mock_post.assert_called_once_with('/backups/12345/restore?restore_original=False', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_restore_original_datastore_object(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        datastore_data = {'id': 'abcdef', 'name': 'ds1'}
        datastore_obj = self.datastores.get_by_data(datastore_data)

        vm_data = [{'id': '12345', 'name': 'vm1'}]
        mock_get.return_value = {virtual_machines.DATA_FIELD: [vm_data]}
        backup_data = {'name': 'name1', 'id': '12345'}
        backup = self.backups.get_by_data(backup_data)
        vm = backup.restore(False, "vm1", datastore_obj)
        self.assertIsInstance(vm, virtual_machines.VirtualMachine)
        self.assertEqual(vm.data, vm_data)

        data = {'virtual_machine_name': 'vm1', 'datastore_id': 'abcdef'}
        mock_post.assert_called_once_with('/backups/12345/restore?restore_original=False', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_lock(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        resource_data = {'name': 'name1', 'id': '12345', 'expiration_time': 'NA'}
        mock_get.return_value = {backups.DATA_FIELD: [resource_data]}
        backup_data = {'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-17T03:59:32Z'}
        backup = self.backups.get_by_data(backup_data)
        backup_obj = backup.lock()
        self.assertEqual(backup_obj.data, resource_data)

        mock_post.assert_called_once_with('/backups/12345/lock', None, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_rename(self, mock_get, mock_post):
        resource_data = {'name': 'backup1', 'id': '12345'}
        backup = self.backups.get_by_data(resource_data)
        backup_data = {'name': 'renamed_backup1', 'id': '12345'}
        mock_get.return_value = {backups.DATA_FIELD: [backup_data]}
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_obj = backup.rename(backup_data['name'])
        self.assertIsInstance(backup_obj, backups.Backup)
        self.assertEqual(backup_obj.data["name"], backup_data['name'])
        mock_post.assert_called_once_with('/backups/12345/rename',
                                          {'backup_name': backup_data['name']},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_copy_cluster_object(self, mock_get, mock_post):
        resource_data = {'name': 'backup1', 'id': '12345', 'omnistack_cluster_id': 'cluster0'}
        backup = self.backups.get_by_data(resource_data)
        backup_data = {'name': 'backup1', 'id': '67890', 'omnistack_cluster_id': 'cluster1'}
        mock_get.return_value = {backups.DATA_FIELD: [backup_data]}
        mock_post.return_value = None, [{'object_id': '12345'}]
        cluster_data = {'name': 'cluster1', 'id': '67890'}
        cluster = self.clusters.get_by_data(cluster_data)

        copy_backup = backup.copy(cluster)
        self.assertIsInstance(copy_backup, backups.Backup)
        self.assertEqual(copy_backup.data, backup_data)
        mock_post.assert_called_once_with('/backups/12345/copy',
                                          {'destination_id': '67890'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_copy_cluster_name(self, mock_get, mock_post):
        resource_data = {'name': 'backup1', 'id': '12345', 'omnistack_cluster_id': 'cluster0'}
        cluster_data = {'name': 'cluster1', 'id': '67890'}
        backup = self.backups.get_by_data(resource_data)
        backup_data = {'name': 'backup1', 'id': '67890', 'omnistack_cluster_id': 'cluster1'}
        mock_get.side_effect = [{omnistack_clusters.DATA_FIELD: [cluster_data]},
                                {backups.DATA_FIELD: [backup_data]}]
        mock_post.return_value = None, [{'object_id': '12345'}]
        copy_backup = backup.copy(cluster_data['name'])
        self.assertIsInstance(copy_backup, backups.Backup)
        self.assertEqual(copy_backup.data, backup_data)
        mock_post.assert_called_once_with('/backups/12345/copy',
                                          {'destination_id': '67890'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_copy_external_store(self, mock_get, mock_post):
        resource_data = {'name': 'backup1', 'id': '12345', 'external_store_name': ''}
        backup = self.backups.get_by_data(resource_data)
        backup_data = {'name': 'backup1', 'id': '67890', 'external_store_name': 'storeonce_catalyst_ds'}
        mock_get.return_value = {backups.DATA_FIELD: [backup_data]}
        mock_post.return_value = None, [{'object_id': '12345'}]

        copy_backup = backup.copy(external_store_name='storeonce_catalyst_ds')
        self.assertIsInstance(copy_backup, backups.Backup)
        self.assertEqual(copy_backup.data, backup_data)
        mock_post.assert_called_once_with('/backups/12345/copy',
                                          {'external_store_name': 'storeonce_catalyst_ds'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_retention_force_false_cluster_obj(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = [{'name': 'name1', 'id': '12345', 'expiration_time': 'NA'},
                       {'name': 'name2', 'id': '67890', 'expiration_time': 'NA'}]
        backup_ret_data = [{'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-22T15:51:56Z'},
                           {'name': 'name2', 'id': '67890', 'expiration_time': '2020-05-22T15:51:56Z'}]
        backup_list = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data['id'] for backup in backup_list]
        cluster_group_data = {"id": "12345", 'name': 'cluster_group1'}
        cluster_group = self.cluster_groups.get_by_data(cluster_group_data)
        mock_get.return_value = {backups.DATA_FIELD: backup_ret_data}
        backup_obj = self.backups.set_retention(backup_list, 10, False, cluster_group)
        self.assertIsInstance(backup_obj[0], backups.Backup)
        self.assertEqual(backup_obj[0].data, backup_ret_data[0])
        data = {'backup_id': backup_ids, 'retention': 10, 'force': False, 'cluster_group_id': "12345"}
        mock_post.assert_called_once_with('/backups/set_retention', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_retention_force_true_cluster_obj(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = [{'name': 'name1', 'id': '12345', 'expiration_time': 'NA'},
                       {'name': 'name2', 'id': '67890', 'expiration_time': 'NA'}]
        backup_ret_data = [{'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-22T15:51:56Z'},
                           {'name': 'name2', 'id': '67890', 'expiration_time': '2020-05-22T15:51:56Z'}]
        backup_list = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data['id'] for backup in backup_list]
        cluster_group_data = {"id": "12345", 'name': 'cluster_group1'}
        cluster_group = self.cluster_groups.get_by_data(cluster_group_data)
        mock_get.return_value = {backups.DATA_FIELD: backup_ret_data}
        backup_obj = self.backups.set_retention(backup_list, 10, True, cluster_group)
        self.assertIsInstance(backup_obj[0], backups.Backup)
        self.assertEqual(backup_obj[0].data, backup_ret_data[0])
        data = {'backup_id': backup_ids, 'retention': 10, 'force': True, 'cluster_group_id': "12345"}
        mock_post.assert_called_once_with('/backups/set_retention', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_retention_force_true_cluster_name(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = [{'name': 'name1', 'id': '12345', 'expiration_time': 'NA'},
                       {'name': 'name2', 'id': '67890', 'expiration_time': 'NA'}]
        backup_ret_data = [{'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-22T15:51:56Z'},
                           {'name': 'name2', 'id': '67890', 'expiration_time': '2020-05-22T15:51:56Z'}]
        backup_list = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data['id'] for backup in backup_list]
        resource_data = [{'id': '12345', 'name': 'cluster_group1'}]
        mock_get.side_effect = [{cluster_groups.DATA_FIELD: resource_data}, {backups.DATA_FIELD: backup_ret_data}]
        backup_obj = self.backups.set_retention(backup_list, 10, True, '12345')
        self.assertIsInstance(backup_obj[0], backups.Backup)
        self.assertEqual(backup_obj[0].data, backup_ret_data[0])
        data = {'backup_id': backup_ids, 'retention': 10, 'force': True, 'cluster_group_id': "12345"}
        mock_post.assert_called_once_with('/backups/set_retention', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_retention_force_false_cluster_name(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = [{'name': 'name1', 'id': '12345', 'expiration_time': 'NA'},
                       {'name': 'name2', 'id': '67890', 'expiration_time': 'NA'}]
        backup_ret_data = [{'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-22T15:51:56Z'},
                           {'name': 'name2', 'id': '67890', 'expiration_time': '2020-05-22T15:51:56Z'}]
        backup_list = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data['id'] for backup in backup_list]
        resource_data = [{'id': '12345', 'name': 'cluster_group1'}]
        mock_get.side_effect = [{cluster_groups.DATA_FIELD: resource_data}, {backups.DATA_FIELD: backup_ret_data}]
        backup_obj = self.backups.set_retention(backup_list, 10, False, '12345')
        self.assertIsInstance(backup_obj[0], backups.Backup)
        self.assertEqual(backup_obj[0].data, backup_ret_data[0])
        data = {'backup_id': backup_ids, 'retention': 10, 'force': False, 'cluster_group_id': "12345"}
        mock_post.assert_called_once_with('/backups/set_retention', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_retention_force_true_cluster_none(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = [{'name': 'name1', 'id': '12345', 'expiration_time': 'NA'},
                       {'name': 'name2', 'id': '67890', 'expiration_time': 'NA'}]
        backup_ret_data = [{'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-22T15:51:56Z'},
                           {'name': 'name2', 'id': '67890', 'expiration_time': '2020-05-22T15:51:56Z'}]
        backup_list = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data['id'] for backup in backup_list]
        mock_get.return_value = {backups.DATA_FIELD: backup_ret_data}
        backup_obj = self.backups.set_retention(backup_list, 10, True)
        self.assertIsInstance(backup_obj[0], backups.Backup)
        self.assertEqual(backup_obj[0].data, backup_ret_data[0])
        data = {'backup_id': backup_ids, 'retention': 10, 'force': True}
        mock_post.assert_called_once_with('/backups/set_retention', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_retention_force_false_cluster_none(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        backup_data = [{'name': 'name1', 'id': '12345', 'expiration_time': 'NA'},
                       {'name': 'name2', 'id': '67890', 'expiration_time': 'NA'}]
        backup_ret_data = [{'name': 'name1', 'id': '12345', 'expiration_time': '2020-05-22T15:51:56Z'},
                           {'name': 'name2', 'id': '67890', 'expiration_time': '2020-05-22T15:51:56Z'}]
        backup_list = [self.backups.get_by_data(entry) for entry in backup_data]
        backup_ids = [backup.data['id'] for backup in backup_list]
        mock_get.return_value = {backups.DATA_FIELD: backup_ret_data}
        backup_obj = self.backups.set_retention(backup_list, 10)
        self.assertIsInstance(backup_obj[0], backups.Backup)
        self.assertEqual(backup_obj[0].data, backup_ret_data[0])
        data = {'backup_id': backup_ids, 'retention': 10, 'force': False}
        mock_post.assert_called_once_with('/backups/set_retention', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_cancel(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        resource_data = {'name': 'name1', 'id': '12345', 'state': 'SAVING'}
        mock_get.return_value = {backups.DATA_FIELD: [resource_data]}
        backup_data = {'name': 'name1', 'id': '12345', 'state': 'CANCELED'}
        backup = self.backups.get_by_data(backup_data)
        backup_obj = backup.cancel()
        self.assertEqual(backup_obj.data, resource_data)
        mock_post.assert_called_once_with('/backups/12345/cancel', None, custom_headers=None)

    @mock.patch.object(Connection, "get")
    def test_get_virtual_disk_partitions(self, mock_get):
        resource_data = {"partitions": [{
                         "partition_number": 1,
                         "size": 32868352,
                         "disk_type": "BIOS",
                         "mountable": True
                         }]}
        mock_get.return_value = resource_data
        backup_data = {'name': 'name1', 'id': '12345'}
        backup = self.backups.get_by_data(backup_data)
        virtual_disk = "tinyvm32_ATF_0.vmdk"
        partition_data = backup.get_virtual_disk_partitions(virtual_disk)
        self.assertEqual(partition_data, resource_data)
        mock_get.assert_has_calls([call('/backups/12345/virtual_disk_partitions?virtual_disk=tinyvm32_ATF_0.vmdk')])

    @mock.patch.object(Connection, "get")
    def test_get_virtual_disk_partition_files(self, mock_get):
        resource_data = {"virtual_disk_partition_files": [{
                         "name": "grub",
                         "directory": True,
                         "symbolic_link": False,
                         "size": 0,
                         "last_modified": "2013-01-18T14:51:43Z",
                         "file_level_restore_available": True
                         }]}
        mock_get.return_value = resource_data
        backup_data = {'name': 'name1', 'id': '12345'}
        backup = self.backups.get_by_data(backup_data)
        virtual_disk = "tinyvm32_ATF_0.vmdk"
        partition_number = 1
        file_path = "/"
        partition_data = backup.get_virtual_disk_partition_files(virtual_disk, partition_number, file_path)
        self.assertEqual(partition_data, resource_data)
        mock_get.assert_has_calls([call('/backups/12345/virtual_disk_partition_files?file_path=%2F&partition_number=1&virtual_disk=tinyvm32_ATF_0.vmdk')])

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_restore_files(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        resource_data = {'name': 'name1', 'id': '12345', 'state': 'PROTECTED'}
        mock_get.return_value = {backups.DATA_FIELD: [resource_data]}
        backup_data = {'name': 'name1', 'id': '12345', 'state': 'PROTECTED'}
        backup = self.backups.get_by_data(backup_data)
        paths = ['vmdkName/partition/file1', 'vmdkName/partition/directory/file2']
        backup.restore_files("12345", paths)
        data = {"virtual_machine_id": "12345", "paths": ['vmdkName/partition/file1', 'vmdkName/partition/directory/file2']}
        mock_post.assert_called_once_with('/backups/12345/restore_files', data, custom_headers={'Content-type': 'application/vnd.simplivity.v1.9+json'})


if __name__ == '__main__':
    unittest.main()
