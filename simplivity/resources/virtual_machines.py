###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
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

"""Implements features available for Virtual Machine resource."""

from simplivity.resources.resource import ResourceBase
from simplivity.resources import datastores
from simplivity.resources import omnistack_clusters
from simplivity.resources import backups
from simplivity.resources import policies

URL = '/virtual_machines'
DATA_FIELD = 'virtual_machines'


class VirtualMachines(ResourceBase):
    """Implements features for SympliVity VM resources."""

    def __init__(self, connection):
        """Initialize VirtualMachines class."""
        super(VirtualMachines, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True, show_optional_fields=False):
        """Get all vms.

        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs.
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
              id: The unique identifier (UID) of the virtual_machines to return
                Accepts: Single value, comma-separated list
              name: The name of the virtual_machines to return
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              omnistack_cluster_id: The unique identifier (UID) of the omnistack_cluste
                that is associated with the instances to return
                Accepts: Single value, comma-separated list
              omnistack_cluster_name: The name of the omnistack_cluster that
                is associated with the instances to return.
                Accepts: Single value, comma-separated list.
              compute_cluster_parent_hypervisor_object_id: The unique identifier (UID)
                of the hypervisor that contains the omnistack_cluster that is associated
                with the instances to return
                Accepts: Single value, comma-separated list.
              compute_cluster_parent_name: The name of the hypervisor that contains the
                omnistack_cluster that is associated with the instances to return
                Accepts: Single value, comma-separated list
              hypervisor_management_system: The IP address of the hypervisor associated
                with the virtual machine.
                Accepts: Single value, comma-separated list, pattern using one
                or more asterisk characters as a wildcard
              hypervisor_management_system_name: The name of the hypervisor associated
                with the virtual machine
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              datastore_id: The unique identifier (UID) of the datastore that is associated
                with the instances to return
                Accepts: Single value, comma-separated list
              datastore_name: The name of the datastore that is associated with the
                instances to return
                Accepts: Single value, comma-separated list
              policy_id: The unique identifier (UID) of the policy that is associated
                with the instances to return
                Accepts: Single value, comma-separated list
              policy_name: The name of the policy that is associated with the instances to return
                Accepts: Single value, comma-separated list
              hypervisor_object_id: The unique identifier (UID) of the hypervisor-based instance
                that is associated with the instances to return
                Accepts: Single value, comma-separated list
              created_after: The earliest creation time after the virtual machines to return were
                created, expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              created_before: The latest creation time before the virtual machines to return were
                created, expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              state: The state of the virtual_machine that is associated with the instances to return
                Accepts: Single value, comma-separated list
              app_aware_vm_status: The status of the ability of the virtual machine to take
                an application-consistent backup that uses Microsoft VSS
                Accepts: Single value, comma-separated list
              hypervisor_is_template: An indicator that shows if the virtual machine is a template.
              host_id: The unique identifier (UID) of the virtual_machine host.
            fields: A comma-separated list of fields to include in the returned objects
            case_sensitive: An indicator that specifies if the filter and sort results
              use a case-sensitive or insensitive manner.
            show_optional_fields: An indicator to show or not show the ha_status,
              ha_resynchronization_progress, hypervisor_virtual_machine_power_state,
              and hypervisor_is_template.

        Returns:
            list/pagination object: list of VirtualMachine objects/ Pagination object
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
                                    case_sensitive=case_sensitive,
                                    show_optional_fields=show_optional_fields)

    def get_by_data(self, data):
        """Gets VM object from VM data.

        Args:
            data: VM data

        Returns:
            object: Virtual Machine object.
        """
        return VirtualMachine(self._connection, self._client, data)

    def set_policy_for_multiple_vms(self, policy, vms, timeout=-1):
        """Sets the backup policy for virtual machines.

        Args:
            vms: list of vm objects
            policy: policy object
        """
        method_url = "{}/set_policy".format(URL)

        vm_ids = [vm.data["id"] for vm in vms]
        policy_id = policy.data["id"]
        data = {"virtual_machine_id": vm_ids,
                "policy_id": policy_id}

        affected_resources = self._client.do_post(method_url, data, timeout, None)

        vm_ids = [resource["object_id"] for resource in affected_resources]
        comma_separated_ids = ','.join(vm_ids)

        return self.get_all(filters={'id': comma_separated_ids})


class VirtualMachine(object):
    """Implements features available for a single VM."""

    def __init__(self, connection, resource_client, data):
        """Initialize with connection object, resource client and VM data"""
        self.data = data
        self._connection = connection
        self._client = resource_client
        self._vms = VirtualMachines(self._connection)

    def __refresh(self):
        """Updates the VM data."""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self.data = self._client.do_get(resource_uri)

    def clone(self, new_vm_name, app_consistent=False, datastore=None, timeout=-1):
        """Clones a virtual machine.

        Args:
            new_vm_name: The name of the virtual_machine created from this action.
            app_consistent: An indicator to show if the backup represents a snapshot
              of a virtual machine with data that was first flushed to disk.
            datastore: Object/name of the datastore.
              if passed, new VM will be moved to the datastore.
            timeout: Time out for the request in seconds.

        Returns:
            object: Object of the new VM
        """
        method_url = "{}/{}/clone".format(URL, self.data["id"])
        data = {"virtual_machine_name": new_vm_name,
                "app_consistent": app_consistent}

        out = self._client.do_post(method_url, data, timeout, None)
        vm = self._vms.get_by_id(out[0]["object_id"])

        if datastore:
            return vm.move(new_vm_name, datastore)

        return vm

    def move(self, new_vm_name, datastore, timeout=-1):
        """Moves a virtual machine to another datastore.

        Args:
            new_vm_name: Name of the new vm
            datastore: Object/name of the destination datastore
            timeout: Time out for the request in seconds.

        Returns:
            VirtualMachine object: Object of the moved VM
        """
        method_url = "{}/{}/move".format(URL, self.data["id"])

        if not isinstance(datastore, datastores.Datastore):
            # if passed name of the datastore
            datastores_obj = datastores.Datastores(self._connection)
            datastore = datastores_obj.get_by_name(datastore)

        data = {"virtual_machine_name": new_vm_name,
                "destination_datastore_id": datastore.data["id"]}

        affected_object = self._client.do_post(method_url, data, timeout, None)[0]
        vm_obj = self._vms.get_by_id(affected_object["object_id"])
        self.data = vm_obj.data

        return self

    def create_backup(self, backup_name, cluster=None, app_consistent=False,
                      consistency_type=None, retention=0, timeout=-1):
        """Backs up a virtual machine.

        Args:
            backup_name: The name of the new backup created from this action.
            cluster: Destination OmnistackCluster object/name.
            app_consistent: An indicator to show if the backup represents
              a snapshot of a virtual machine with data that was first flushed to disk.
            consistency_type: The consistency type of the backup.
            retention: The number of minutes to keep backups.
            timeout: Time out for the request in seconds.

        Returns:
            Backup object: object of the newly created backup.
        """
        method_url = "{}/{}/backup".format(URL, self.data["id"])

        if cluster and not isinstance(cluster, omnistack_clusters.OmnistackCluster):
            # if passed name of the omnistack cluster
            clusters_obj = omnistack_clusters.OmnistackClusters(self._connection)
            cluster = clusters_obj.get_by_name(cluster)

        data = {"backup_name": backup_name,
                "app_consistent": app_consistent,
                "consistency_type": consistency_type,
                "retention": retention}

        if cluster:
            data["destination_id"] = cluster.data["id"]

        backup = self._client.do_post(method_url, data, timeout, None)[0]
        return backups.Backups(self._connection).get_by_id(backup["object_id"])

    def get_backups(self):
        """Retrieves all backups associated with this virtual_machine.

        Returns:
            list: List of backup objects
        """
        method_url = "{}/{}/backups".format(URL, self.data["id"])
        backup_data = self._client.do_get(method_url).get("backups", [])

        backup_objs = []
        for backup in backup_data:
            obj = backups.Backups(self._connection).get_by_id(backup["id"])
            backup_objs.append(obj)

        return backup_objs

    def set_backup_parameters(self, guest_username, guest_password, override_guest_validation=False,
                              app_aware_type=None, timeout=-1):
        """Set the virtual machine backup parameters used for application consistent backups.

        Args:
            guest_username: Username of the virtual machine.
            guest_password: Password of the virtual machine.
            override_guest_validation: Set to true to disable virtual machine validation logic.
            app_aware_type: Set the application aware backup type:
              VSS - Application-consistentbackup using Microsoft VSS
              DEFAULT - Crash-consistent
              NONE - Application-consistent backup using a VMware snapshot
            timeout: Time out for the request in seconds.

        Returns:
            self: Returns the same object.
        """
        method_url = "{}/{}/backup_parameters".format(URL, self.data["id"])

        data = {"guest_username": guest_username,
                "guest_password": guest_password,
                "override_guest_validation": override_guest_validation,
                "app_aware_type": app_aware_type}

        self._client.do_post(method_url, data, timeout, None)
        self.__refresh()

        return self

    def set_policy(self, policy, timeout=-1):
        """Sets the backup policy for virtual machine.

        Args:
            policy: Policy object/name
            timeout: Time out for the request in seconds.

        Returns:
            self: Returns the same object.
        """
        method_url = "{}/{}/set_policy".format(URL, self.data["id"])

        if not isinstance(policy, policies.Policy):
            # if passed name of the policy
            policy = policies.Policies(self._connection).get_by_name(policy)

        data = {"policy_id": policy.data["id"]}

        self._client.do_post(method_url, data, timeout, None)
        self.__refresh()

        return self
