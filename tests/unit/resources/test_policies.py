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
from urllib.parse import quote_plus

from simplivity.connection import Connection
from simplivity import exceptions
from simplivity.resources import policies
from simplivity.resources import virtual_machines
from simplivity.resources import omnistack_clusters as clusters
from simplivity.resources import hosts
from simplivity.resources import cluster_groups


class PoliciesTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.policies = policies.Policies(self.connection)
        self.clusters = clusters.OmnistackClusters(self.connection)
        self.hosts = hosts.Hosts(self.connection)
        self.cluster_groups = cluster_groups.ClusterGroups(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(policies.URL)
        resource_data = [{'id': '12345'}, {'id': '67890'}]
        mock_get.return_value = {policies.DATA_FIELD: resource_data}

        objs = self.policies.get_all()
        self.assertIsInstance(objs[0], policies.Policy)
        self.assertEqual(objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_found(self, mock_get):
        name = "testname"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(policies.URL, name)
        resource_data = [{'id': '12345', 'name': name}]
        mock_get.return_value = {policies.DATA_FIELD: resource_data}

        obj = self.policies.get_by_name(name)
        self.assertIsInstance(obj, policies.Policy)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_name_not_found(self, mock_get):
        name = "testname"
        resource_data = []
        mock_get.return_value = {policies.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.policies.get_by_name(name)

        self.assertEqual(error.exception.msg, "Resource not found with the name {}".format(name))

    @mock.patch.object(Connection, "get")
    def test_get_by_name_url_encoded(self, mock_get):
        name = "test name"
        url = "{}?case=sensitive&limit=500&name={}&offset=0&order=descending&sort=name".format(policies.URL, quote_plus(name))
        resource_data = [{'id': '12345', 'name': name}]
        mock_get.return_value = {policies.DATA_FIELD: resource_data}

        obj = self.policies.get_by_name(name)
        self.assertIsInstance(obj, policies.Policy)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_id_found(self, mock_get):
        resource_id = "12345"
        url = "{}?case=sensitive&id={}&limit=500&offset=0&order=descending&sort=name".format(policies.URL, resource_id)
        resource_data = [{'id': resource_id}]
        mock_get.return_value = {policies.DATA_FIELD: resource_data}

        obj = self.policies.get_by_id(resource_id)
        self.assertIsInstance(obj, policies.Policy)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_by_id_not_found(self, mock_get):
        resource_id = "12345"
        resource_data = []
        mock_get.return_value = {policies.DATA_FIELD: resource_data}

        with self.assertRaises(exceptions.HPESimpliVityResourceNotFound) as error:
            self.policies.get_by_id(resource_id)

        self.assertEqual(error.exception.msg, "Resource not found with the id {}".format(resource_id))

    def test_get_by_data(self):
        resource_data = {'id': '12345'}

        obj = self.policies.get_by_data(resource_data)
        self.assertIsInstance(obj, policies.Policy)
        self.assertEqual(obj.data, resource_data)

    @mock.patch.object(Connection, "delete")
    def test_delete(self, mock_delete):
        mock_delete.return_value = None, [{'object_id': '12345'}]

        policy_data = {'name': 'name1', 'id': '12345'}
        policy = self.policies.get_by_data(policy_data)

        policy.delete()
        mock_delete.assert_called_once_with('/policies/12345', custom_headers=None)

    @mock.patch.object(Connection, "get")
    def test_get_vms(self, mock_get):
        resource_data = [{'id': '12345'}, {'id': '67890'}]
        mock_get.return_value = {"virtual_machines": resource_data}

        policy_data = {'name': 'name1', 'id': 'ABCDE'}
        policy = self.policies.get_by_data(policy_data)

        vms = policy.get_vms()
        self.assertEqual(resource_data[0].get('id'), vms[0].data['id'])
        for vm in vms:
            self.assertIsInstance(vm, virtual_machines.VirtualMachine)

        mock_get.assert_called_once_with('/policies/ABCDE/virtual_machines')

    @mock.patch.object(Connection, "get")
    def test_get_vms_not_found(self, mock_get):
        resource_data = []
        mock_get.return_value = {"virtual_machines": resource_data}

        policy_data = {'name': 'name1', 'id': 'ABCDE'}
        policy = self.policies.get_by_data(policy_data)

        vms = policy.get_vms()
        self.assertEqual(vms, [])

        mock_get.assert_called_once_with('/policies/ABCDE/virtual_machines')

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_policy(self, mock_get, mock_post):
        resource_data = [{'name': 'test', 'id': '12345'}]
        mock_get.return_value = {policies.DATA_FIELD: resource_data}
        mock_post.return_value = None, [{'object_id': '12345'}]
        policy_name = 'test'
        policy = self.policies.create(policy_name)
        data = {'name': 'test'}
        self.assertIsInstance(policy, policies.Policy)
        self.assertEqual(policy.data, resource_data[0])
        mock_post.assert_called_once_with('/policies', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_multiple_rules(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': 'policy12345'}]
        resources_data = {"rules": [{"frequency": 5, "id": "12345", "retention": 1},
                                    {"frequency": 10, "id": "67890", "retention": 2}], "name": "name",
                          "id": "policy12345"}

        mock_get.return_value = {'policy': resources_data}
        policy_obj = self.policies.get_by_data({'id': 'policy12345', 'name': 'name'})
        rules = [
            {
                "frequency": 1,
                "retention": 5
            },
            {
                "frequency": 10,
                "retention": 2
            }
        ]
        policy_obj.create_rules(rules)
        self.assertEqual(policy_obj.data, resources_data)
        mock_post.assert_called_once_with('/policies/policy12345/rules?replace_all_rules=False', rules,
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_single_rules(self, mock_get, mock_post):
        mock_post.return_value = None, [{'object_id': 'policy12345'}]
        resources_data = {"rules": [{"frequency": 5, "id": "12345", "retention": 1}], "name": "name",
                          "id": "policy12345"}

        mock_get.return_value = {'policy': resources_data}
        policy_obj = self.policies.get_by_data({'id': 'policy12345', 'name': 'name'})
        rules = {
            "frequency": 1,
            "retention": 5
        }
        policy_obj.create_rules(rules)
        self.assertEqual(policy_obj.data, resources_data)
        mock_post.assert_called_once_with('/policies/policy12345/rules?replace_all_rules=False', [rules],
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_create_policy_with_flags(self, mock_get, mock_post):
        policy_name = 'policy0'
        resource_data = [{'name': policy_name, 'id': '12345'}]
        mock_get.return_value = {policies.DATA_FIELD: resource_data}
        mock_post.return_value = None, [{'object_id': '12345'}]
        policy = self.policies.create(policy_name, flags={'cluster_group_id': 'abcdefg'})
        self.assertIsInstance(policy, policies.Policy)
        self.assertEqual(policy.data, resource_data[0])
        mock_post.assert_called_once_with('/policies?cluster_group_id=abcdefg', {'name': policy_name}, custom_headers=None)

    @mock.patch.object(Connection, "get")
    def test_get_rule(self, mock_get):
        resources_data = [{'frequency': 1, 'retention': 5, 'id': 12345}]
        mock_get.return_value = {"rules": resources_data}
        policy_obj = self.policies.get_by_data({'id': '67890', 'name': 'name', 'rules': resources_data})
        policy_obj.get_rule(12345)
        self.assertEqual(policy_obj.data['rules'], resources_data)

    @mock.patch.object(Connection, "delete")
    @mock.patch.object(Connection, "get")
    def test_delete_rule(self, mock_get, mock_delete):
        mock_delete.return_value = None, [{'object_id': '67890'}]
        resources_data = {"rules": [], "name": "name", "id": "67890"}
        mock_get.return_value = {'policy': resources_data}
        policy_data = {"rules": [{"frequency": 5, "id": "12345", "retention": 1}], "name": "name",
                       "id": "67890"}

        policy = self.policies.get_by_data(policy_data)

        response_policy = policy.delete_rule(12345)
        self.assertEqual(response_policy.data, resources_data)
        mock_delete.assert_called_once_with('/policies/67890/rules/12345', custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_suspend_host(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        host_data = {"id": "12345", 'name': 'host1'}
        host = self.hosts.get_by_data(host_data)

        self.policies.suspend(host)
        data = {'target_object_id': '12345',
                'target_object_type': 'host'}
        mock_post.assert_called_once_with('/policies/suspend', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_suspend_cluster(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        cluster_data = {"id": "12345", 'name': 'cluster1'}
        cluster = self.clusters.get_by_data(cluster_data)

        self.policies.suspend(cluster)
        data = {'target_object_id': '12345',
                'target_object_type': 'omnistack_cluster'}
        mock_post.assert_called_once_with('/policies/suspend', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_suspend_cluster_group(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        cluster_group_data = {"id": "12345", 'name': 'cluster_group1'}
        cluster_group = self.cluster_groups.get_by_data(cluster_group_data)

        self.policies.suspend(cluster_group)
        data = {'target_object_id': '12345',
                'target_object_type': 'cluster_group'}
        mock_post.assert_called_once_with('/policies/suspend', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_suspend_federation(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        self.policies.suspend()
        data = {'target_object_type': 'federation'}
        mock_post.assert_called_once_with('/policies/suspend', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_rename(self, mock_get, mock_post):
        resource_data = {'name': 'policy0', 'id': '12345'}
        policy = self.policies.get_by_data(resource_data)
        policy_data = {'name': 'renamed_policy0', 'id': '12345'}
        mock_get.return_value = {'policy': policy_data}
        mock_post.return_value = None, [{'object_id': '12345'}]
        policy = policy.rename(policy_data['name'])
        self.assertIsInstance(policy, policies.Policy)
        self.assertEqual(policy.data["name"], policy_data['name'])
        mock_post.assert_called_once_with('/policies/12345/rename',
                                          {'name': policy_data['name']},
                                          custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_resume_federation(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        self.policies.resume()
        data = {'target_object_type': 'federation'}
        mock_post.assert_called_once_with('/policies/resume', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_resume_with_cluster(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        cluster_data = {"id": "12345", 'name': 'cluster1'}
        cluster = self.clusters.get_by_data(cluster_data)
        self.policies.resume(cluster)
        data = {'target_object_id': '12345',
                'target_object_type': 'omnistack_cluster'}
        mock_post.assert_called_once_with('/policies/resume', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_resume_host(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        host_data = {"id": "12345", 'name': 'host1'}
        host = self.hosts.get_by_data(host_data)
        self.policies.resume(host)
        data = {'target_object_id': '12345',
                'target_object_type': 'host'}
        mock_post.assert_called_once_with('/policies/resume', data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    def test_policies_resume_cluster_group(self, mock_post):
        mock_post.return_value = None, [{'object_id': '12345'}]
        cluster_group_data = {"id": "12345", 'name': 'cluster_group1'}
        cluster_group = self.cluster_groups.get_by_data(cluster_group_data)
        self.policies.resume(cluster_group)
        data = {'target_object_id': '12345',
                'target_object_type': 'cluster_group'}
        mock_post.assert_called_once_with('/policies/resume', data, custom_headers=None)

    @mock.patch.object(Connection, "put")
    @mock.patch.object(Connection, "get")
    def test_edit_rule(self, mock_get, mock_put):
        mock_put.return_value = None, [{'object_id': '67890'}]
        updated_rule = {'frequency': 10, 'retention': 50}
        resources_data = {"rules": [updated_rule], "name": "policy1", "id": "67890"}
        mock_get.return_value = {'policy': resources_data}
        policy_data = {"rules": [{"frequency": 5, "id": "12345", "retention": 1}], "name": "policy1",
                       "id": "67890"}
        policy = self.policies.get_by_data(policy_data)

        response_policy = policy.edit_rule(12345, updated_rule)
        self.assertEqual(response_policy.data, resources_data)
        mock_put.assert_called_once_with('/policies/67890/rules/12345', updated_rule, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_create_rules(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345"}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        rules = {
            "frequency": 1,
            "retention": 5
        }
        report = policy_obj.impact_create_rules(rules)
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/impact_report/create_rules?replace_all_rules=False', [rules],
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.14+json"})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_create_replace_rules(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345"}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        rules = {
            "frequency": 1,
            "retention": 5
        }
        report = policy_obj.impact_create_rules(rules, replace_all_rules=True)
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/impact_report/create_rules?replace_all_rules=True', [rules],
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.14+json"})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_create_multiple_rules(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345"}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        rules = [{"frequency": 5, "retention": 1},
                 {"frequency": 10, "retention": 2}]
        report = policy_obj.impact_create_rules(rules)
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/impact_report/create_rules?replace_all_rules=False', rules,
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.14+json"})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_edit_rules(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345"}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        rules = {
            "rule_id": "123456",
            "frequency": 2,
            "retention": 6
        }
        report = policy_obj.impact_edit_rules(rules)
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/impact_report/edit_rules?replace_all_rules=False', [rules],
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.14+json"})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_edit_replace_rules(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345"}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        rules = {
            "rule_id": "123456",
            "frequency": 10,
            "retention": 5
        }
        report = policy_obj.impact_edit_rules(rules, replace_all_rules=True)
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/impact_report/edit_rules?replace_all_rules=True', [rules],
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.14+json"})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_edit_multiple_rules(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345"}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        rules = [{"rule_id": "123456", "frequency": 5, "retention": 1},
                 {"rule_id": "123457", "frequency": 10, "retention": 2}]
        report = policy_obj.impact_edit_rules(rules)
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/impact_report/edit_rules?replace_all_rules=False', rules,
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.14+json"})

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_impact_report_delete_rule(self, mock_get, mock_post):
        data = {"projected_retained_backups_level": 0, "daily_backup_rate": 2, "backup_rate_level": 0,
                "projected_retained_backups": 0, "daily_backup_rate_limit": 217, "retained_backups_limit": 75}
        resource_data = {"schedule_after_change": data, "schedule_before_change": data}
        mock_post.return_value = None, resource_data
        policy_data = {"name": "policy1", "id": "12345", "rules": [{"id": "56789"}]}

        mock_get.return_value = {'policy': policy_data}
        policy_obj = self.policies.get_by_data(policy_data)
        report = policy_obj.impact_report_delete_rule("56789")
        self.assertEqual(report, resource_data)
        mock_post.assert_called_once_with('/policies/12345/rules/56789/impact_report/delete_rule', None,
                                          custom_headers={"Content-type": "application/vnd.simplivity.v1.9+json"})


if __name__ == '__main__':
    unittest.main()
