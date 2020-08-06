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

"""Implements operations for policies."""

from simplivity.resources.resource import ResourceBase
from simplivity.resources import virtual_machines
from simplivity.resources.hosts import Host
from simplivity.resources.omnistack_clusters import OmnistackCluster
from simplivity.resources.cluster_groups import ClusterGroup

URL = '/policies'
DATA_FIELD = 'policies'


class Policies(ResourceBase):
    """Implements features for SimpliVity Policy resources."""

    def __init__(self, connection):
        super(Policies, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True):
        """Gets all policies.

        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs.
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
              id: The unique identifier (UID) of the policy
                Accepts: Single value, comma-separated list
              name:The name of the policy
                Accepts: Single value, comma-separated list
        Returns:
          list: list of Policy objects
        """
        return self._client.get_all(URL,
                                    members_field=DATA_FIELD,
                                    pagination=pagination,
                                    page_size=page_size,
                                    limit=limit,
                                    offset=offset,
                                    sort=sort,
                                    order=order,
                                    filters=filters,
                                    fields=fields,
                                    case_sensitive=case_sensitive)

    def get_by_data(self, data):
        """Gets Policy object from data.

        Args:
            data: Policy data

        Returns:
            object: Policy object.
        """
        return Policy(self._connection, self._client, data)

    def create(self, name, flags=None, timeout=-1):
        """ create the new policy

        Args:
            name : The name of the new policy created from this action.
            flags: Dictionary of flags. Example: {'cluster_group_id': 'cluster_group_id'}
            timeout : Time out for the request in seconds.

        Returns:
            object: Policy object.
        """
        data = {"name": name}

        affected_object = self._client.do_post(URL, data, timeout, flags=flags)[0]
        return self.get_by_id(affected_object["object_id"])

    def suspend(self, target=None, timeout=-1):
        """Suspends policy-based backups on a specific targeted object
            Args:
                target: Target object.
                        Allowed object of host, omnistack_cluster, cluster_group and default is federation
                timeout: Time out for the request in seconds.

            Returns:
                None
        """
        data = {}
        if isinstance(target, (Host, OmnistackCluster, ClusterGroup)):
            data["target_object_type"] = target.OBJECT_TYPE
            data["target_object_id"] = target.data["id"]
        else:
            data["target_object_type"] = 'federation'

        resource_uri = "{}/suspend".format(URL)
        self._client.do_post(resource_uri, data, timeout)

    def resume(self, target=None, timeout=-1):
        """Resumes policy-based backups on a specific targeted object
            Args:
                target: Target object.
                        Allowed object of host, omnistack_cluster, cluster_group and default is federation
                timeout: Time out for the request in seconds.

            Returns:
                None
        """
        data = {}
        if isinstance(target, (Host, OmnistackCluster, ClusterGroup)):
            data["target_object_type"] = target.OBJECT_TYPE
            data["target_object_id"] = target.data["id"]
        else:
            data["target_object_type"] = 'federation'

        method_url = "{}/resume".format(URL)
        self._client.do_post(method_url, data, timeout)


class Policy(object):
    """Implements features available for a single Policy resource."""

    OBJECT_TYPE = "policy"

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client

    def __refresh(self):
        """Updates the policy data."""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self.data = self._client.do_get(resource_uri)[self.OBJECT_TYPE]

    def get_vms(self):
        """Retrieves the virtual machines using this policy.

        Returns:
          list: List of vms.
        """
        method_url = "{}/{}/virtual_machines".format(URL, self.data["id"])
        vm_data = self._client.do_get(method_url).get("virtual_machines", [])

        vms_obj = virtual_machines.VirtualMachines(self._connection)
        vms = []

        for vm in vm_data:
            vms.append(vms_obj.get_by_data(vm))

        return vms

    def delete(self, timeout=-1):
        """Removes a policy"""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self._client.do_delete(resource_uri, timeout, None)
        self.data = None

    def create_rules(self, rules, replace_all_rules=False, timeout=-1):
        """Creates one or more new rules or replaces existing rules with new rules for a policy

        Args:
            rules: Array of rules.(below are the parameter that can be passed in the array)
                [Mandatory Parameters]
                frequency: The number of minutes between backups
                retention: The number of minutes to keep backups
                [Optional Parameters]
                application_consistent: Set false for crash-consistent backups
                                        Set true for application-consistent backups (for example, VSS or snapshot backups)
                                        Default: false
                consistency_type: Set to DEFAULT for a snapshot backup
                                  Set to VSS for a Microsoft Volume Shadow Copy Service backup
                                  Set to NONE for crash-consistent backups
                                  Default: NONE
                destination_id: The unique identifier (UID) of the omnistack_cluster to store the backup
                                Default: local omnistack_cluster
                days: The days of the week (for example, Mon,Fri), or month (for example, 1,15) to take backups or
                      "last" to specify the last day of each month
                      Default: All (that is, every day)
                start_time: The time to start the backups, for example, 14:30
                            This time is local to the time zone of the Hypervisor Management System (HMS)
                            Default: 00:00
                end_time: The time to stop backing up, for example, 14:30
                          This time is local to the time zone of the Hypervisor Management System (HMS)
                          Default: 00:00
                external_store_name: The name of the external_store

            replace_all_rules: If set to True, replaces the existing rules with new rules
                               If set to False, adds the new rules to existing set of rules
            timeout: Time out for the request in seconds.


        Returns:
            self: Returns the policy object.
        """
        resource_uri = "{}/{}/rules".format(URL, self.data["id"])
        if isinstance(rules, dict):
            rules = [rules]

        flags = {'replace_all_rules': replace_all_rules}
        self._client.do_post(resource_uri, rules, timeout, None, flags)[0]

        self.__refresh()

        return self

    def delete_rule(self, rule_id, timeout=-1):
        """Removes a policy rule
        Args:
            rule_id: Rule id to be deleted
            timeout: Time out for the request in seconds.

        Returns:
            self: Returns the policy object.
        """
        resource_uri = "{}/{}/rules/{}".format(URL, self.data["id"], rule_id)
        self._client.do_delete(resource_uri, timeout, None)
        self.__refresh()

        return self

    def get_rule(self, rule_id):
        """Retrieves the specified policy rule
           Args:
                rule_id : Rule id to be retrieved

           Returns:
                Rules object
        """
        resource_uri = "{}/{}/rules/{}".format(URL, self.data["id"], rule_id)
        return self._client.do_get(resource_uri)

    def rename(self, new_name, timeout=-1):
        """Renames the specified policy
        Args:
            new_name: The new name of the specified policy.
            timeout: Time out for the request in seconds.

        Returns:
            object: Policy object.
        """

        resource_uri = "{}/{}/rename".format(URL, self.data["id"])

        data = {'name': new_name}
        self._client.do_post(resource_uri, data, timeout)
        self.__refresh()

        return self

    def edit_rule(self, rule_id, rule, timeout=-1):
        """Edits an existing policy rule
        Args:
            rule_id: Rule id to be edited
            rule: Dictionary of fields from backup policy rule can change, except destination_name, id, number,
                  and max_backups.
                application_consistent: Set false for crash-consistent backups
                                        Set true for application-consistent backups (for example, VSS or snapshot backups)
                                        Default: false
                consistency_type: Set to DEFAULT for a snapshot backup
                                  Set to VSS for a Microsoft Volume Shadow Copy Service backup
                                  Set to NONE for crash-consistent backups
                                  Default: NONE
                destination_id: The unique identifier (UID) of the omnistack_cluster to store the backup
                                Default: local omnistack_cluster
                days: The days of the week (for example, Mon,Fri), or month (for example, 1,15) to take backups or
                      "last" to specify the last day of each month
                      Default: All (that is, every day)
                frequency: The number of minutes between backups
                retention: The number of minutes to keep backups
                start_time: The time to start the backups, for example, 14:30
                            This time is local to the time zone of the Hypervisor Management System (HMS)
                            Default: 00:00
                end_time: The time to stop backing up, for example, 14:30
                          This time is local to the time zone of the Hypervisor Management System (HMS)
                          Default: 00:00
                external_store_name: The name of the external_store

            timeout: Time out for the request in seconds.

        Returns:
            self: Returns the policy object.
        """
        resource_uri = "{}/{}/rules/{}".format(URL, self.data["id"], rule_id)
        self._client.do_put(resource_uri, rule, timeout)
        self.__refresh()

        return self

    def impact_create_rules(self, rules, replace_all_rules=False, timeout=-1):
        """Generate a backup impact reported based on proposed creation of rules for the policy

        Args:
            rules: Array of rules.(below are the parameter that can be passed in the array)
                [Mandatory Parameters]
                frequency: The number of minutes between backups
                retention: The number of minutes to keep backups
                [Optional Parameters]
                application_consistent: Set false for crash-consistent backups
                                        Set true for application-consistent backups (for example, VSS or snapshot backups)
                                        Default: false
                consistency_type: Set to DEFAULT for a snapshot backup
                                  Set to VSS for a Microsoft Volume Shadow Copy Service backup
                                  Set to NONE for crash-consistent backups
                                  Default: NONE
                destination_id: The unique identifier (UID) of the omnistack_cluster to store the backup
                                Default: local omnistack_cluster
                days: The days of the week (for example, Mon,Fri), or month (for example, 1,15) to take backups or
                      "last" to specify the last day of each month
                      Default: All (that is, every day)
                start_time: The time to start the backups, for example, 14:30
                            This time is local to the time zone of the Hypervisor Management System (HMS)
                            Default: 00:00
                end_time: The time to stop backing up, for example, 14:30
                          This time is local to the time zone of the Hypervisor Management System (HMS)
                          Default: 00:00
                external_store_name: The name of the external_store

            replace_all_rules: If set to True, replaces the existing rules with new rules
                               If set to False, adds the new rules to existing set of rules
            timeout: Time out for the request in seconds.

        Returns:
            dict : Returns the dictionary for impact report of created rules.
        """
        resource_uri = "{}/{}/impact_report/create_rules".format(URL, self.data["id"])
        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.14+json'}
        if isinstance(rules, dict):
            rules = [rules]

        flags = {'replace_all_rules': replace_all_rules}

        return self._client.do_post(resource_uri, rules, timeout, custom_headers, flags)

    def impact_edit_rules(self, rules, replace_all_rules=False, timeout=-1):
        """Generate a backup impact reported based on proposed changes to the rules for the policy
        Args:
          rules: Array of rules.(below are the parameter that can be passed in the array)
            [Mandatory Parameters]
            rule_id: The unique identifier (UID) of the policy rule
            frequency: The number of minutes between backups
            retention: The number of minutes to keep backups
            [Optional Parameters]
            application_consistent: Set false for crash-consistent backups
                                    Set true for application-consistent backups (for example, VSS or snapshot backups)
                                    Default: false
            consistency_type: Set to DEFAULT for a snapshot backup
                              Set to VSS for a Microsoft Volume Shadow Copy Service backup
                              Set to NONE for crash-consistent backups
                              Default: NONE
            destination_id: The unique identifier (UID) of the omnistack_cluster to store the backup
                            Default: local omnistack_cluster
            days: The days of the week (for example, Mon,Fri), or month (for example, 1,15) to take backups or
                  "last" to specify the last day of each month
                  Default: All (that is, every day)
            start_time: The time to start the backups, for example, 14:30
                        This time is local to the time zone of the Hypervisor Management System (HMS)
                        Default: 00:00
            end_time: The time to stop backing up, for example, 14:30
                      This time is local to the time zone of the Hypervisor Management System (HMS)
                      Default: 00:00
            external_store_name: The name of the external_store

          replace_all_rules: If set to True, replaces the existing rules with new rules
                             If set to False, adds the new rules to existing set of rules
          timeout: Time out for the request in seconds.

        Returns:
          dict : Returns the dictionary for impact report of rules.
        """
        resource_uri = "{}/{}/impact_report/edit_rules".format(URL, self.data["id"])
        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.14+json'}

        if isinstance(rules, dict):
            rules = [rules]
        flags = {'replace_all_rules': replace_all_rules}

        return self._client.do_post(resource_uri, rules, timeout, custom_headers, flags)

    def impact_report_delete_rule(self, rule_id, timeout=-1):
        """Generate a backup impact reported based on proposed deletion of a policy rule
        Args:
          rule_id: The unique identifier (UID) of the policy rule you want to access
          timeout: Time out for the request in seconds.

        Returns:
          dict : Returns the dictionary for impact report of rules.
        """
        resource_uri = "{}/{}/rules/{}/impact_report/delete_rule".format(URL, self.data["id"], rule_id)
        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.9+json'}

        return self._client.do_post(resource_uri, None, timeout, custom_headers)

    def policy_schedule_report(self, cluster_group_id=None):
        """Retrieves the policy schedule report

           Args:
                cluster_group_id: Unique identifier of cluster group

           Returns:
                dict: Dictionary for policy schedule report
        """
        resource_uri = "{}/policy_schedule_report".format(URL)
        data = {}
        if cluster_group_id:
            data = {"cluster_group_id": cluster_group_id}

        return self._client.do_get(resource_uri, data)
