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

import io
import sys
import unittest
from unittest import mock

from simplivity import exceptions
from simplivity.connection import Connection
from simplivity.ovc_client import OVC
from simplivity.resources.backups import Backups
from simplivity.resources.cluster_groups import ClusterGroups
from simplivity.resources.datastores import Datastores
from simplivity.resources.hosts import Hosts
from simplivity.resources.omnistack_clusters import OmnistackClusters
from simplivity.resources.policies import Policies
from simplivity.resources.virtual_machines import VirtualMachines
from simplivity.resources.external_stores import ExternalStores

OS_ENVIRON_CREDENTIALS = {
    'SIMPLIVITYSDK_USERNAME': 'simplicity',
    'SIMPLIVITYSDK_PASSWORD': 'root',
}

OS_ENVIRON_CONFIG = {
    'SIMPLIVITYSDK_OVC_IP': '127.0.0.1',
    'SIMPLIVITYSDK_SSL_CERTIFICATE': 'certificate',
    'SIMPLIVITYSDK_CONNECTION_TIMEOUT': '-1'
}


def mock_builtin(method_name='open'):
    package_name = 'builtins' if sys.version_info[:3] >= (3,) else '__builtin__'
    return "%s.%s" % (package_name, method_name)


class OVCTest(unittest.TestCase):
    @mock.patch.object(Connection, 'login')
    def setUp(self, mock_login):
        super(OVCTest, self).setUp()

        config = {"ip": "127.0.0.1",
                  "credentials": {
                      "username": "simplivity",
                      "password": "root"}}

        self._ovc = OVC(config)

    def __mock_file_open(self, json_config_content):
        return io.StringIO(json_config_content)

    @mock.patch.object(Connection, 'login')
    @mock.patch(mock_builtin('open'))
    def test_from_json_file(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "127.0.0.1",
          "credentials": {
            "username": "simplicity",
            "password": "root"
          }
        }"""
        mock_open.return_value = self.__mock_file_open(json_config_content)
        ovc_client = OVC.from_json_file("config.json")

        self.assertIsInstance(ovc_client, OVC)
        self.assertEqual("127.0.0.1", ovc_client.connection._ovc_ip)

    @mock.patch.object(Connection, 'login')
    @mock.patch.dict('os.environ', {**OS_ENVIRON_CONFIG, **OS_ENVIRON_CREDENTIALS})
    def test_from_environment_variables(self, mock_login):
        OVC.from_environment_variables()
        mock_login.assert_called_once_with('simplicity', 'root')

    @mock.patch.dict('os.environ', {**OS_ENVIRON_CONFIG, **OS_ENVIRON_CREDENTIALS})
    @mock.patch.object(OVC, '__init__')
    def test_from_environment_variables_is_passing_right_arguments_to_the_constructor(self, mock_cls):
        mock_cls.return_value = None
        OVC.from_environment_variables()
        mock_cls.assert_called_once_with({'timeout': '-1',
                                          'ip': '127.0.0.1',
                                          'ssl_certificate': 'certificate',
                                          'credentials': {'username': 'simplicity',
                                                          'password': 'root'}})

    @mock.patch.object(Connection, 'login')
    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG)
    def test_missing_required_environment_variables_missing(self, mock_login):
        with self.assertRaises(exceptions.HPESimpliVityException) as error:
            OVC.from_environment_variables()

        self.assertEqual(error.exception.msg, "Make sure you have set mandatory env variables \
            (SIMPLIVITYSDK_OVC_IP, SIMPLIVITYSDK_USERNAME, SIMPLIVITYSDK_PASSWORD)")

    @mock.patch.object(Connection, 'login')
    def test_credentials_not_provided(self, mock_login):
        print("targeted test")
        config = {"ip": "172.0.0.1"}

        with self.assertRaises(exceptions.HPESimpliVityException) as error:
            OVC(config)

        self.assertEqual(error.exception.msg, "Credentials not provided")

    def test_virtual_machines_has_right_type(self):
        self.assertIsInstance(self._ovc.virtual_machines, VirtualMachines)

    def test_virtual_machines_has_value(self):
        self.assertIsNotNone(self._ovc.virtual_machines)

    def test_lazy_loading_virtual_machines(self):
        virtual_machines = self._ovc.virtual_machines
        self.assertEqual(virtual_machines, self._ovc.virtual_machines)

    def test_policies_has_right_type(self):
        self.assertIsInstance(self._ovc.policies, Policies)

    def test_policies_has_value(self):
        self.assertIsNotNone(self._ovc.policies)

    def test_lazy_loading_policies(self):
        policies = self._ovc.policies
        self.assertEqual(policies, self._ovc.policies)

    def test_datastores_has_right_type(self):
        self.assertIsInstance(self._ovc.datastores, Datastores)

    def test_datastores_has_value(self):
        self.assertIsNotNone(self._ovc.datastores)

    def test_lazy_loading_datastores(self):
        datastores = self._ovc.datastores
        self.assertEqual(datastores, self._ovc.datastores)

    def test_omnistack_clusters_has_right_type(self):
        self.assertIsInstance(self._ovc.omnistack_clusters, OmnistackClusters)

    def test_omnistack_clusters_has_value(self):
        self.assertIsNotNone(self._ovc.omnistack_clusters)

    def test_lazy_loading_omnistack_clusters(self):
        omnistack_clusters = self._ovc.omnistack_clusters
        self.assertEqual(omnistack_clusters, self._ovc.omnistack_clusters)

    def test_backups_has_right_type(self):
        self.assertIsInstance(self._ovc.backups, Backups)

    def test_backups_has_value(self):
        self.assertIsNotNone(self._ovc.backups)

    def test_lazy_loading_backups(self):
        backups = self._ovc.backups
        self.assertEqual(backups, self._ovc.backups)

    def test_hosts_has_right_type(self):
        self.assertIsInstance(self._ovc.hosts, Hosts)

    def test_hosts_has_value(self):
        self.assertIsNotNone(self._ovc.hosts)

    def test_lazy_loading_hosts(self):
        hosts = self._ovc.hosts
        self.assertEqual(hosts, self._ovc.hosts)

    def test_cluster_groups_has_right_type(self):
        self.assertIsInstance(self._ovc.cluster_groups, ClusterGroups)

    def test_cluster_groups_has_value(self):
        self.assertIsNotNone(self._ovc.cluster_groups)

    def test_lazy_loading_cluster_groups(self):
        cluster_groups = self._ovc.cluster_groups
        self.assertEqual(cluster_groups, self._ovc.cluster_groups)

    def test_external_groups_has_right_type(self):
        self.assertIsInstance(self._ovc.external_stores, ExternalStores)

    def test_external_groups_has_value(self):
        self.assertIsNotNone(self._ovc.external_stores)

    def test_lazy_loading_external_groups(self):
        external_stores = self._ovc.external_stores
        self.assertEqual(external_stores, self._ovc.external_stores)


if __name__ == '__main__':
    unittest.main()
