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

from simplivity.connection import Connection
from simplivity import exceptions
from simplivity.resources import datastores
from simplivity.resources import policies
from simplivity.resources import omnistack_clusters as clusters


class DatastoresTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.clusters = clusters.OmnistackClusters(self.connection)
        self.datastores = datastores.Datastores(self.connection)
        self.policies = policies.Policies(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(datastores.URL)
        resource_data = [{'id': '12345'}, {'id': '67890'}]
        mock_get.return_value = {datastores.DATA_FIELD: resource_data}

        objs = self.datastores.get_all()
        self.assertIsInstance(objs[0], datastores.Datastore)
        self.assertEqual(objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_found(self, mock_get):
        name = "testname"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(datastores.URL, name)
        resource_data = [{'id': '12345', 'name': name}]
        mock_get.return_value = {datastores.DATA_FIELD: resource_data}

        obj = self.datastores.get_by_name(name)
        self.assertIsInstance(obj, datastores.Datastore)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_not_found(self, mock_get):
        name = "testname"
        resource_data = []
        mock_get.return_value = {datastores.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.datastores.get_by_name(name)

        self.assertEqual(error.exception.msg, "Resource not found with the name {}".format(name))

    @mock.patch.object(Connection, "get")
    def test_get_by_id_found(self, mock_get):
        resource_id = "12345"
        url = "{}?case=sensitive&id={}&limit=500&offset=0&order=descending&sort=name".format(datastores.URL, resource_id)
        resource_data = [{'id': resource_id}]
        mock_get.return_value = {datastores.DATA_FIELD: resource_data}

        obj = self.datastores.get_by_id(resource_id)
        self.assertIsInstance(obj, datastores.Datastore)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_id_not_found(self, mock_get):
        resource_id = "12345"
        resource_data = []
        mock_get.return_value = {datastores.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.datastores.get_by_id(resource_id)

        self.assertEqual(error.exception.msg, "Resource not found with the id {}".format(resource_id))

    def test_get_by_data(self):
        resource_data = {'id': '12345'}

        obj = self.datastores.get_by_data(resource_data)
        self.assertIsInstance(obj, datastores.Datastore)
        self.assertEqual(obj.data, resource_data)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_using_objects(self, mock_get, mock_post):
        cluster_data = {'name': 'cluster1', 'id': '12345'}
        cluster_obj = self.clusters.get_by_data(cluster_data)

        policy_data = {'name': 'policy1', 'id': '67890'}
        policy_obj = self.policies.get_by_data(policy_data)

        datastore_data = {'name': 'datastore1', 'id': 'ABCDEF'}
        datastore_size = 1024

        mock_post.return_value = None, [{'object_id': datastore_data['id']}]
        mock_get.return_value = {datastores.DATA_FIELD: [datastore_data]}

        datastore = self.datastores.create(datastore_data['name'], cluster_obj, policy_obj, datastore_size)

        self.assertIsInstance(datastore, datastores.Datastore)
        self.assertEqual(datastore.data, datastore_data)
        mock_post.assert_called_once_with('/datastores',
                                          {
                                              'name': 'datastore1',
                                              'omnistack_cluster_id': '12345',
                                              'policy_id': '67890',
                                              'size': 1024
                                          },
                                          custom_headers=None
                                          )

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_using_names(self, mock_get, mock_post):
        cluster_data = {'name': 'cluster1', 'id': '12345'}

        policy_data = {'name': 'policy1', 'id': '67890'}

        datastore_data = {'name': 'datastore1', 'id': 'ABCDEF'}
        datastore_size = 1024

        mock_post.return_value = None, [{'object_id': datastore_data['id']}]
        mock_get.side_effect = [{clusters.DATA_FIELD: [cluster_data]}, {policies.DATA_FIELD: [policy_data]}, {datastores.DATA_FIELD: [datastore_data]}]

        datastore = self.datastores.create(datastore_data['name'], cluster_data['name'], policy_data['name'], datastore_size)

        self.assertIsInstance(datastore, datastores.Datastore)
        self.assertEqual(datastore.data, datastore_data)
        mock_post.assert_called_once_with('/datastores',
                                          {
                                              'name': 'datastore1',
                                              'omnistack_cluster_id': '12345',
                                              'policy_id': '67890',
                                              'size': 1024
                                          },
                                          custom_headers=None
                                          )

    @mock.patch.object(Connection, "delete")
    def test_delete(self, mock_delete):
        mock_delete.return_value = None, [{'object_id': '12345'}]

        datastore_data = {'name': 'name1', 'id': '12345'}
        datastore = self.datastores.get_by_data(datastore_data)

        datastore.delete()
        mock_delete.assert_called_once_with('/datastores/12345', custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_resize(self, mock_get, mock_post):
        resource_data = [{'id': '12345', 'name': 'ds1', 'size': 2048}]
        mock_get.return_value = {datastores.DATA_FIELD: resource_data}
        mock_post.return_value = None, [{'object_id': '12345'}]
        datastore_data = {'name': 'name1', 'id': '12345', 'size': 1024}
        datastore = self.datastores.get_by_data(datastore_data)
        datastore.resize(2048)
        self.assertIsInstance(datastore, datastores.Datastore)
        self.assertEqual(datastore.data, resource_data[0])
        mock_post.assert_called_once_with('/datastores/12345/resize', {'size': 2048}, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_policy_with_policy_name(self, mock_get, mock_post):
        resource_data = {'name': 'ds1', 'id': '12345', 'policy_id': '4567'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        policy_name = 'policy1'
        mock_get.side_effect = [{'policies': [{'name': policy_name, 'id': '4567'}]},
                                {'datastore': resource_data}]

        datastore_data = {'name': 'ds1', 'id': '12345', 'policy_id': '7890'}
        datastore = self.datastores.get_by_data(datastore_data)
        datastore.set_policy(policy_name)
        self.assertIsInstance(datastore, datastores.Datastore)
        self.assertEqual(datastore.data, resource_data)

        mock_post.assert_called_once_with('/datastores/12345/set_policy', {'policy_id': '4567'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_policy_with_policy_obj(self, mock_get, mock_post):
        resource_data = {'name': 'ds1', 'id': '12345', 'policy_id': '7890'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'datastore': resource_data}
        policy_obj = self.policies.get_by_data({'id': '4567', 'name': 'policy1'})

        datastore_data = {'name': 'ds1', 'id': '12345', 'policy_id': '7890'}
        datastore = self.datastores.get_by_data(datastore_data)
        datastore.set_policy(policy_obj)
        self.assertIsInstance(datastore, datastores.Datastore)
        self.assertEqual(datastore.data, resource_data)

        mock_post.assert_called_once_with('/datastores/12345/set_policy', {'policy_id': '4567'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "get")
    def test_standard_hosts(self, mock_get):
        resource_data = {'standard_hosts': [{'hypervisor_object_id': '1234', 'ip_address': '10.1.2.5',
                         'name': 'host', 'shared': False, 'virtual_machine_count': 0}]}
        mock_get.return_value = resource_data

        datastore_data = {'id': '12345'}
        datastore = self.datastores.get_by_data(datastore_data)

        standard_hosts = datastore.standard_hosts()
        self.assertEqual(standard_hosts, resource_data)


if __name__ == '__main__':
    unittest.main()
