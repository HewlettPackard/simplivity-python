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
from simplivity.resources import virtual_machines as machines
from simplivity.resources import policies
from simplivity.resources import datastores
from simplivity.resources import omnistack_clusters


class VirtualMachinesTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.machines = machines.VirtualMachines(self.connection)
        self.policies = policies.Policies(self.connection)
        self.datastores = datastores.Datastores(self.connection)
        self.clusters = omnistack_clusters.OmnistackClusters(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(machines.URL)
        resource_data = [{'id': '12345'}, {'id': '67890'}]
        mock_get.return_value = {machines.DATA_FIELD: resource_data}

        vm_objs = self.machines.get_all()
        self.assertIsInstance(vm_objs[0], machines.VirtualMachine)
        self.assertEqual(vm_objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_found(self, mock_get):
        vm_name = "testname"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(machines.URL, vm_name)
        resource_data = [{'id': '12345', 'name': vm_name}]
        mock_get.return_value = {machines.DATA_FIELD: resource_data}

        vm_obj = self.machines.get_by_name(vm_name)
        self.assertIsInstance(vm_obj, machines.VirtualMachine)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_not_found(self, mock_get):
        vm_name = "testname"
        resource_data = []
        mock_get.return_value = {machines.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.machines.get_by_name(vm_name)

        self.assertEqual(error.exception.msg, "Resource not found with the name {}".format(vm_name))

    @mock.patch.object(Connection, "get")
    def test_get_by_id_found(self, mock_get):
        vm_id = "12345"
        url = "{}?case=sensitive&id={}&limit=500&offset=0&order=descending&sort=name".format(machines.URL, vm_id)
        resource_data = [{'id': vm_id}]
        mock_get.return_value = {machines.DATA_FIELD: resource_data}

        vm_obj = self.machines.get_by_id(vm_id)
        self.assertIsInstance(vm_obj, machines.VirtualMachine)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_id_not_found(self, mock_get):
        vm_id = "12345"
        resource_data = []
        mock_get.return_value = {machines.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.machines.get_by_id(vm_id)

        self.assertEqual(error.exception.msg, "Resource not found with the id {}".format(vm_id))

    def test_get_by_data(self):
        resource_data = {'id': '12345'}

        vm_obj = self.machines.get_by_data(resource_data)
        self.assertIsInstance(vm_obj, machines.VirtualMachine)
        self.assertEqual(vm_obj.data, resource_data)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_policy_for_multiple_vms(self, mock_get, mock_post):
        mock_post.return_value = {}, {}
        vm1_data = {'name': 'name1', 'id': 'id1'}
        vm2_data = {'name': 'name2', 'id': 'id2'}
        vm_objs = [self.machines.get_by_data(vm1_data),
                   self.machines.get_by_data(vm2_data)]
        policy_obj = self.policies.get_by_data({'name': 'name', 'id': 'id'})

        mock_get.side_effect = [vm1_data, vm2_data]

        self.machines.set_policy_for_multiple_vms(policy_obj, vm_objs)
        mock_post.assert_called_once_with('/virtual_machines/set_policy',
                                          {'policy_id': 'id', 'virtual_machine_id': ['id1', 'id2']},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_clone(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machines': {'id': '12345'}}

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.clone('new_vm_name')

        mock_post.assert_called_once_with('/virtual_machines/12345/clone',
                                          {'app_consistent': False, 'virtual_machine_name': 'new_vm_name'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    @mock.patch.object(machines.VirtualMachine, "move")
    def test_clone_with_datastore_name(self, mock_move, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machines': {'id': '12345'}}
        datastore_name = 'testdatastore'
        new_vm_name = "new_vm_name"

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.clone(new_vm_name, datastore=datastore_name)

        mock_post.assert_called_once_with('/virtual_machines/12345/clone',
                                          {'app_consistent': False, 'virtual_machine_name': 'new_vm_name'},
                                          custom_headers=None)

        mock_move.assert_called_once_with(new_vm_name, datastore_name)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_move_with_datastore_name(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.side_effect = [{'datastores': [{'name': 'datastore', 'id': '12345'}]},
                                {'virtual_machines': {'id': '12345'}}]
        new_vm_name = "new_vm_name"
        datastore_name = "datastorename"

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.move(new_vm_name, datastore_name)

        mock_post.assert_called_once_with('/virtual_machines/12345/move',
                                          {'destination_datastore_id': '12345', 'virtual_machine_name': new_vm_name},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_move_with_datastore_obj(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machines': {'id': '12345'}}
        new_vm_name = "new_vm_name"
        datastore_obj = self.datastores.get_by_data({'id': '12345', 'name': 'name'})

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.move(new_vm_name, datastore_obj)

        mock_post.assert_called_once_with('/virtual_machines/12345/move',
                                          {'destination_datastore_id': '12345', 'virtual_machine_name': new_vm_name},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_backup_with_cluster_name(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.side_effect = [{'omnistack_clusters': [{'name': 'name', 'id': '12345'}]},
                                {'backups': {'id': '12345'}}]
        cluster_name = "cluster_name"
        backup_name = "backup name"

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.create_backup(backup_name, cluster_name)

        mock_post.assert_called_once_with('/virtual_machines/12345/backup',
                                          {'app_consistent': False, 'backup_name': 'backup name',
                                           'consistency_type': None, 'destination_id': '12345', 'retention': 0},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_backup_with_cluster_obj(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'backups': {'id': '12345'}}
        backup_name = "backup name"
        cluster_obj = self.clusters.get_by_data({'id': '12345', 'name': 'name'})

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.create_backup(backup_name, cluster_obj)

        mock_post.assert_called_once_with('/virtual_machines/12345/backup',
                                          {'app_consistent': False, 'backup_name': backup_name,
                                           'consistency_type': None, 'destination_id': '12345', 'retention': 0},
                                          custom_headers=None)

    @mock.patch.object(Connection, "get")
    def test_get_backups(self, mock_get):
        mock_get.side_effect = [{'backups': [{'id': '12345'}]}, {'backups': [{'id': '12345'}]}]

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.get_backups()

        mock_get.assert_has_calls([call('/virtual_machines/12345/backups'),
                                   call('/backups?case=sensitive&id=12345&limit=500&offset=0&order=descending&sort=name')])

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_setup_backup_parameters(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machine': [{'name': 'name', 'id': '12345'}]}

        username = "username"
        password = "password"

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.set_backup_parameters(username, password)

        mock_post.assert_called_once_with('/virtual_machines/12345/backup_parameters',
                                          {'app_aware_type': None, 'override_guest_validation': False,
                                           'guest_username': username, 'guest_password': password},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_policy_with_policy_name(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.side_effect = [{'policies': [{'name': 'datastore', 'id': '12345'}]},
                                {'virtual_machine': {'id': '12345'}}]
        policy_name = "policy name"

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.set_policy(policy_name)

        mock_post.assert_called_once_with('/virtual_machines/12345/set_policy', {'policy_id': '12345'},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_set_policy_with_policy_obj(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machine': {'id': '12345'}}
        policy_obj = self.policies.get_by_data({'id': 'policy12345', 'name': 'name'})

        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        vm.set_policy(policy_obj)

        mock_post.assert_called_once_with('/virtual_machines/12345/set_policy',
                                          {'policy_id': 'policy12345'}, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_power_off_success(self, mock_get, mock_post):
        resource_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'OFF'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machine': resource_data}

        vm1_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'ON'}
        vm = self.machines.get_by_data(vm1_data)
        boolreturn = vm.power_off()

        self.assertEqual(vm.data, resource_data)
        self.assertIsInstance(boolreturn, bool)
        mock_post.assert_called_once_with('/virtual_machines/12345/power_off', None, custom_headers={'Content-type': 'application/vnd.simplivity.v1.11+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_power_off_failure(self, mock_get, mock_post):
        resource_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'ON'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machine': resource_data}

        vm1_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'ON'}
        vm = self.machines.get_by_data(vm1_data)
        boolreturn = vm.power_off()

        self.assertEqual(vm.data, resource_data)
        self.assertIsInstance(boolreturn, bool)
        mock_post.assert_called_once_with('/virtual_machines/12345/power_off', None, custom_headers={'Content-type': 'application/vnd.simplivity.v1.11+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_power_on_success(self, mock_get, mock_post):
        resource_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'ON'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machine': resource_data}

        vm1_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'OFF'}
        vm = self.machines.get_by_data(vm1_data)
        boolreturn = vm.power_on()

        self.assertEqual(vm.data, resource_data)
        self.assertIsInstance(boolreturn, bool)
        mock_post.assert_called_once_with('/virtual_machines/12345/power_on', None, custom_headers={'Content-type': 'application/vnd.simplivity.v1.14+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_power_on_failure(self, mock_get, mock_post):
        resource_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'OFF'}
        mock_post.return_value = None, [{'object_id': '12345'}]
        mock_get.return_value = {'virtual_machine': resource_data}

        vm1_data = {'name': 'name1', 'id': '12345', 'hypervisor_virtual_machine_power_state': 'OFF'}
        vm = self.machines.get_by_data(vm1_data)
        ispoweron = vm.power_on()

        self.assertEqual(vm.data, resource_data)
        self.assertIsInstance(ispoweron, bool)
        mock_post.assert_called_once_with('/virtual_machines/12345/power_on', None, custom_headers={'Content-type': 'application/vnd.simplivity.v1.14+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_policy_impact_report(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        vm_data = {'name': 'name1', 'id': 'id1'}
        vm = self.machines.get_by_data(vm_data)
        policy_obj = self.policies.get_by_data({'name': 'name', 'id': 'id'})
        mock_get.side_effect = [{"name": "policy1", "id": "12345"}, [vm]]

        self.machines.policy_impact_report(policy_obj, [vm])
        mock_post.assert_called_once_with('/virtual_machines/policy_impact_report/apply_policy',
                                          {'policy_id': 'id', 'virtual_machine_id': ['id1']},
                                          custom_headers={'Content-type': 'application/vnd.simplivity.v1.14+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_policy_impact_report_with_multiple_vms(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        vm_data = [{'name': 'name1', 'id': 'id1'},
                   {'name': 'name2', 'id': 'id2'}]
        vm_objs = [self.machines.get_by_data(entry) for entry in vm_data]
        policy_obj = self.policies.get_by_data({'name': 'name', 'id': 'id'})
        mock_get.side_effect = [{"name": "policy1", "id": "12345"}, vm_objs]

        self.machines.policy_impact_report(policy_obj, vm_objs)
        mock_post.assert_called_once_with('/virtual_machines/policy_impact_report/apply_policy',
                                          {'policy_id': 'id', 'virtual_machine_id': ['id1', 'id2']},
                                          custom_headers={'Content-type': 'application/vnd.simplivity.v1.14+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_policy_impact_report_with_policy_name(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        vm_data = [{'name': 'name1', 'id': 'id1'},
                   {'name': 'name2', 'id': 'id2'}]
        vm_objs = [self.machines.get_by_data(entry) for entry in vm_data]
        policy_data = [{"name": "policy1", "id": "12345"}]
        mock_get.side_effect = [{policies.DATA_FIELD: policy_data}, vm_objs]

        self.machines.policy_impact_report("policy1", vm_objs)
        mock_post.assert_called_once_with('/virtual_machines/policy_impact_report/apply_policy',
                                          {'policy_id': '12345', 'virtual_machine_id': ['id1', 'id2']},
                                          custom_headers={'Content-type': 'application/vnd.simplivity.v1.14+json'})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_validate_backup_credentials(self, mock_get, mock_post):
        mock_post.return_value = None, {'credentials_validation': {'status': 'VALID'}}
        mock_get.return_value = {'virtual_machine': [{'name': 'name', 'id': '12345'}]}

        username = "username"
        password = "password"
        vm1_data = {'name': 'name1', 'id': '12345'}
        vm = self.machines.get_by_data(vm1_data)
        status = vm.validate_backup_credentials(username, password)

        self.assertEqual(status, 'VALID')
        mock_post.assert_called_once_with('/virtual_machines/12345/validate_backup_credentials', {'guest_username': username, 'guest_password': password},
                                          custom_headers=None)


if __name__ == '__main__':
    unittest.main()
