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
from simplivity.resources import external_stores
from simplivity.resources import omnistack_clusters as clusters


class ExternalStoresTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.external_stores = external_stores.ExternalStores(self.connection)
        self.clusters = clusters.OmnistackClusters(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(external_stores.URL)
        resource_data = [{'name': 'storeonce_catalyst1'}, {'name': 'storeonce_catalyst2'}]
        mock_get.return_value = {external_stores.DATA_FIELD: resource_data}

        external_stores_objs = self.external_stores.get_all()
        self.assertIsInstance(external_stores_objs[0], external_stores.ExternalStore)
        self.assertEqual(external_stores_objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_found(self, mock_get):
        external_store_name = "storeonce_catalyst1"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(external_stores.URL,
                                                                                               external_store_name)
        resource_data = [{'name': external_store_name}]
        mock_get.return_value = {external_stores.DATA_FIELD: resource_data}

        external_store_obj = self.external_stores.get_by_name(external_store_name)
        self.assertIsInstance(external_store_obj, external_stores.ExternalStore)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_not_found(self, mock_get):
        external_store_name = "storeonce_catalyst3"
        resource_data = []
        mock_get.return_value = {external_stores.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.external_stores.get_by_name(external_store_name)

        self.assertEqual(error.exception.msg, "Resource not found with the name {}".format(external_store_name))

    def test_get_by_data(self):
        resource_data = {'name': 'storeonce_catalyst1'}

        external_store_obj = self.external_stores.get_by_data(resource_data)
        self.assertIsInstance(external_store_obj, external_stores.ExternalStore)
        self.assertEqual(external_store_obj.data, resource_data)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_register_external_store_cluster_object(self, mock_get, mock_post):
        cluster_data = {'name': 'cluster1', 'id': '12345'}
        cluster_obj = self.clusters.get_by_data(cluster_data)
        resource_data = {'management_ip': '10.0.75,112', 'name': 'storeonce_cat1'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {external_stores.DATA_FIELD: [resource_data]}
        external_store = self.external_stores.register_external_store('10.0.75,112', 'storeonce_cat1', cluster_obj,
                                                                      'Admin', 'svtrfs')

        self.assertIsInstance(external_store, external_stores.ExternalStore)
        self.assertEqual(external_store.data, resource_data)
        data = {'management_ip': '10.0.75,112', 'management_port': 9387,
                'name': 'storeonce_cat1', 'omnistack_cluster_id': '12345',
                'username': 'Admin', 'password': 'svtrfs', 'storage_port': 9388,
                'type': 'StoreOnceOnPrem'}
        mock_post.assert_called_once_with(external_stores.URL, data,
                                          custom_headers={'Content-type': 'application/vnd.simplivity.v1.11+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_register_external_store_cluster_name(self, mock_get, mock_post):
        cluster_data = {'name': 'cluster1', 'id': '12345'}
        resource_data = {'management_ip': '10.0.75,112', 'name': 'storeonce_cat1'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.side_effect = [{clusters.DATA_FIELD: [cluster_data]}, {external_stores.DATA_FIELD: [resource_data]}]
        external_store = self.external_stores.register_external_store('10.0.75,112', 'storeonce_cat1', 'cluster1',
                                                                      'Admin', 'svtrfs')

        self.assertIsInstance(external_store, external_stores.ExternalStore)
        self.assertEqual(external_store.data, resource_data)
        data = {'management_ip': '10.0.75,112', 'management_port': 9387,
                'name': 'storeonce_cat1', 'omnistack_cluster_id': '12345',
                'username': 'Admin', 'password': 'svtrfs', 'storage_port': 9388,
                'type': 'StoreOnceOnPrem'}
        mock_post.assert_called_once_with(external_stores.URL, data,
                                          custom_headers={'Content-type': 'application/vnd.simplivity.v1.11+json'})


if __name__ == '__main__':
    unittest.main()
