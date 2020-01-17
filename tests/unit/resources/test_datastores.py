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
from simplivity.resources import omnistack_clusters as clusters


class OmnistackClustersTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.clusters = clusters.OmnistackClusters(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(clusters.URL)
        resource_data = [{'id': '12345'}, {'id': '67890'}]
        mock_get.return_value = {clusters.DATA_FIELD: resource_data}

        objs = self.clusters.get_all()
        self.assertIsInstance(objs[0], clusters.OmnistackCluster)
        self.assertEquals(objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_found(self, mock_get):
        name = "testname"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(clusters.URL, name)
        resource_data = [{'id': '12345', 'name': name}]
        mock_get.return_value = {clusters.DATA_FIELD: resource_data}

        obj = self.clusters.get_by_name(name)
        self.assertIsInstance(obj, clusters.OmnistackCluster)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_not_found(self, mock_get):
        name = "testname"
        resource_data = []
        mock_get.return_value = {clusters.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.clusters.get_by_name(name)

        self.assertEquals(error.exception.msg, "Resource not found with the name {}".format(name))

    @mock.patch.object(Connection, "get")
    def test_get_by_id_found(self, mock_get):
        resource_id = "12345"
        url = "{}?case=sensitive&id={}&limit=500&offset=0&order=descending&sort=name".format(clusters.URL, resource_id)
        resource_data = [{'id': resource_id}]
        mock_get.return_value = {clusters.DATA_FIELD: resource_data}

        obj = self.clusters.get_by_id(resource_id)
        self.assertIsInstance(obj, clusters.OmnistackCluster)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_id_not_found(self, mock_get):
        resource_id = "12345"
        resource_data = []
        mock_get.return_value = {clusters.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.clusters.get_by_id(resource_id)

        self.assertEquals(error.exception.msg, "Resource not found with the id {}".format(resource_id))

    def test_get_by_data(self):
        resource_data = {'id': '12345'}

        obj = self.clusters.get_by_data(resource_data)
        self.assertIsInstance(obj, clusters.OmnistackCluster)
        self.assertEquals(obj.data, resource_data)


if __name__ == '__main__':
    unittest.main()
