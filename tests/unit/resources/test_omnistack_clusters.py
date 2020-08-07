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
        self.assertEqual(objs[0].data, resource_data[0])
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

        self.assertEqual(error.exception.msg, "Resource not found with the name {}".format(name))

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

        self.assertEqual(error.exception.msg, "Resource not found with the id {}".format(resource_id))

    def test_get_by_data(self):
        resource_data = {'id': '12345'}

        obj = self.clusters.get_by_data(resource_data)
        self.assertIsInstance(obj, clusters.OmnistackCluster)
        self.assertEqual(obj.data, resource_data)

    @mock.patch.object(Connection, "get")
    def test_get_time_zones(self, mock_get):
        resource_data = [
            "America/Denver",
            "America/New_York"
        ]
        mock_get.return_value = resource_data
        time_zones = self.clusters.get_time_zone_list()
        self.assertEqual(time_zones, resource_data)

    @mock.patch.object(Connection, "get")
    def test_get_connected_clusters(self, mock_get):
        mock_get.side_effect = [{'omnistack_clusters': [{'id': '12345'}]}, {'omnistack_clusters': [{'id': '12345'}]}]

        cluster_data = {'name': 'name1', 'id': '12345'}
        cluster = self.clusters.get_by_data(cluster_data)
        obj = cluster.get_connected_clusters()
        self.assertIsInstance(obj[0], clusters.OmnistackCluster)
        mock_get.assert_has_calls([call('/omnistack_clusters/12345/connected_clusters'),
                                  call('/omnistack_clusters?case=sensitive&id=12345&limit=500&offset=0&order=descending&sort=name')])

    @mock.patch.object(Connection, "get")
    def test_get_throughput_without_filters(self, mock_get):
        cluster_data = {'name': 'name1', 'id': '12345'}
        resource_data = {'start_time': '2020-06-09T01:10:55Z', 'end_time': '2020-06-09T13:10:55Z',
                         'cluster_throughput': [{'average_throughput': '12345',
                                                 'data': {'date_of_minimum': '2020-06-09T11:45:00Z',
                                                          'minimum_throughput': '141',
                                                          'date_of_maximum': '2020-06-09T11:41:00Z',
                                                          'maximum_throughput': '3298',
                                                          'data_points': [
                                                              {'value': '3298', 'date': '2020-06-09T11:41:00Z'},
                                                              {'value': '814', 'date': '2020-06-09T11:42:00Z'}]}}]}

        mock_get.return_value = resource_data
        cluster = self.clusters.get_by_data(cluster_data)
        obj = cluster.get_throughput()
        self.assertEqual(obj, resource_data)
        mock_get.assert_has_calls([call('/omnistack_clusters/12345/throughput?range=43200&time_offset=0')])

    @mock.patch.object(Connection, "get")
    def test_get_throughput_with_filters(self, mock_get):
        cluster_data = {'name': 'name1', 'id': '12345'}
        resource_data = {'start_time': '2020-06-09T01:10:55Z', 'end_time': '2020-06-09T13:10:55Z',
                         'cluster_throughput': [{'source_omnistack_cluster_id': '12345',
                                                 'destination_omnistack_cluster_id': '123456',
                                                 'average_throughput': '12345',
                                                 'data': {'date_of_minimum': '2020-06-09T11:45:00Z',
                                                          'minimum_throughput': '141',
                                                          'date_of_maximum': '2020-06-09T11:41:00Z',
                                                          'maximum_throughput': '3298',
                                                          'data_points': [
                                                              {'value': '3298', 'date': '2020-06-09T11:41:00Z'},
                                                              {'value': '814', 'date': '2020-06-09T11:42:00Z'}]}}]}

        mock_get.return_value = resource_data
        cluster = self.clusters.get_by_data(cluster_data)
        obj = cluster.get_throughput("123456", 0, 200)

        self.assertEqual(obj, resource_data)
        mock_get.assert_has_calls([call('/omnistack_clusters/12345/throughput?destination_id=123456&range=200&time_offset=0')])

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_time_zone(self, mock_get, mock_post):
        resource_data = {'id': '12345', 'name': 'name1', 'time_zone': 'Zulu'}
        mock_get.return_value = {'omnistack_cluster': {'id': '12345', 'name': 'name1', 'time_zone': 'Africa/Accra'}}
        mock_post.return_value = None, [{'object_id': '12345'}]
        cluster = self.clusters.get_by_data(resource_data)
        cluster_obj = cluster.set_time_zone("Africa/Accra")
        self.assertEqual(cluster_obj.data['time_zone'], "Africa/Accra")
        data = {'time_zone': 'Africa/Accra'}
        mock_post.assert_called_once_with('/omnistack_clusters/12345/set_time_zone', data, custom_headers=None)

    @mock.patch.object(Connection, "get")
    def test_get_metrics(self, mock_get):
        resource_data = {"metrics": [{"name": "iops",
                                      "data_points": [{
                                          "reads": 0,
                                          "writes": 0,
                                          "date": "2020-06-22T14:05:00Z"
                                      }]
                                      }]
                         }
        mock_get.return_value = resource_data
        cluster_data = {'name': 'cluster', 'id': '12345'}
        cluster = self.clusters.get_by_data(cluster_data)
        response = cluster.get_metrics()
        self.assertEqual(response, resource_data)
        mock_get.assert_has_calls([call('/omnistack_clusters/12345/metrics?range=43200&resolution=MINUTE&time_offset=0')])


if __name__ == '__main__':
    unittest.main()
