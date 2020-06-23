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

from simplivity.resources.resource import ResourceBase
from simplivity.resources import datastores
from simplivity.resources import virtual_machines
from simplivity.resources import omnistack_clusters
from simplivity.resources import cluster_groups

URL = '/backups'
DATA_FIELD = 'backups'


class Backups(ResourceBase):
    """Implements features available for SimpliVity Backup resources."""

    def __init__(self, connection):
        super(Backups, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True):
        """Gets all backups.

        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs.
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
              id: the unique identifier (UID) of the backups to return
                Accepts: Single value, comma-separated list
              name: The name of the backups to return
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard.
              sent_min: The minimum sent data size (in bytes) of the remote backups to return.
              sent_max: The maximum sent data size (in bytes) of the remote backups to return.
              state: The current state of the backups to return
                Accepts: Single value, comma-separated list
              type: The type of backups to return.
                Accepts: Single value, comma-separated list.
              omnistack_cluster_id: The unique identifier (UID) of the omnistack_cluster
                that is associated with the instances to return
                Accepts: Single value, comma-separated list
              omnistack_cluster_name: The name of the omnistack_cluster that is associated
                with the instances to return
                Accepts: Single value, comma-separated list
              compute_cluster_parent_hypervisor_object_id: The unique identifier (UID) of the
                hypervisor that contains the omnistack_cluster that is associated with the instances to return
                Accepts: Single value, comma-separated list
              compute_cluster_parent_name: The name of the hypervisor that contains the
                omnistack_cluster that is associated with the instances to return
                Accepts: Single value, comma-separated list
              datastore_id: The unique identifier (UID) of the datastore that is associated
                with the instances to return
                Accepts: Single value, comma-separated list
              datastore_name: The name of the datastore that is associated with the instances to return
                Accepts: Single value, comma-separated list
              expires_before: The latest expiration time before the backups to return expire,
                expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              expires_after: The earliest expiration time after the backups to return expire,
                expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              virtual_machine_id: The unique identifier (UID) of the virtual_machine that is
                associated with the instances to return
                Accepts: Single value, comma-separated list
              virtual_machine_name: The name of the virtual_machine that is associated with
                the instances to return
                Accepts: Single value, comma-separated list
              virtual_machine_type: The type of the virtual_machine that is associated with the
                instances to return
                Accepts: Single value, comma-separated list
              size_min: The minimum size (in bytes) of the backups to return
              size_max: The maximum size (in bytes) of the backups to return
              application_consistent: The application-consistent setting of the backups to return
              consistency_type: The consistency type of the backups to return
                Accepts: Single value, comma-separated list
              created_before: The latest creation time before the backups to return were created,
                expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              created_after: The earliest creation time after the backups to return were created,
                expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              sent_duration_min: The minimum number of seconds that elapsed while replicating
                the backups to return
              sent_duration_max: The maximum number of seconds that elapsed while replicating the
                backups to return
              sent_completion_before: The latest time before the replication of backups to return was
                completed, expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              sent_completion_after: The earliest time after the replication of backups to return was
                completed, expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)

        Returns:
          list: list of resources
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
        """Gets Backup object from backup data.

        Args:
            data: Backup data

        Returns:
            object: Backup object.
        """
        return Backup(self._connection, self._client, data)

    def delete_multiple_backups(self, backups, timeout=-1):
        """Deletes a list of backups.

        Args:
          backups: list of backup objects
        """
        method_url = "{}/delete".format(URL)

        backup_ids = [backup.data["id"] for backup in backups]
        data = {"backup_id": backup_ids}

        self._client.do_post(method_url, data, timeout, None)

    def set_retention(self, backups, retention, force=False, cluster_group=None, timeout=-1):
        """Sets the retention time for the specified list of backups.

        Args:
          backups: The list of backup objects that you want to set the retention time for.
          retention: The number of minutes to keep backups.
          force: An indicator to force a retention time modification even if this action results in deleting backups.
            Valid Values:
              True: Sets the new retention time for the specified list of backups. This action may delete of one or more
                    backups.
              False: Does not make the requested retention time modification if this results in deleting one or more
                     backups. This operation returns a list of backups that the requested modification deletes. If the
                     requested modification does not delete the backups, the retention time modification occurs.
          cluster_group: Object/name of the cluster group.
          timeout: Time out for the request in seconds.

        Returns:
          list: List of backup objects.
        """
        method_url = "{}/set_retention".format(URL)
        backup_ids = [backup.data["id"] for backup in backups]
        data = {"backup_id": backup_ids, "retention": retention, "force": force}

        if cluster_group:
            if not isinstance(cluster_group, cluster_groups.ClusterGroup):
                # if passed by cluster_group name
                cluster_group = cluster_groups.ClusterGroups(self._connection).get_by_name(cluster_group)
            cluster_group_id = cluster_group.data["id"]
            data["cluster_group_id"] = cluster_group_id
        self._client.do_post(method_url, data, timeout)
        comma_separated_ids = ','.join(backup_ids)

        return self.get_all(filters={'id': comma_separated_ids})


class Backup(object):
    """Implements features available for a single Backup resources."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
        self._backups = Backups(self._connection)

    def __refresh(self):
        """Updates the backup data."""
        resource_object = self._backups.get_by_id(self.data["id"])
        self.data = resource_object.data

    def delete(self, timeout=-1):
        """Deletes the specified backup"""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self._client.do_delete(resource_uri, timeout, None)
        self.data = None

    def restore(self, restore_original, virtual_machine_name=None, datastore=None, timeout=-1):
        """Creates a new virtual machine or replaces the original virtual machine from the specified backup

        Args:
           restore_original: If True, Resets the original virtual machine to the same state it was in when the backup was created
                             If False, Creates a new virtual machine from the backup with the provided name, optionally to a different datastore
           virtual_machine_name: The name of the new virtual machine created from this action.
           datastore: Destination datastore object/name.
           timeout: Time out for the request in seconds.

        Returns:
              Virtual machine object

        """
        resource_uri = "{}/{}/restore".format(URL, self.data["id"])
        data = {}
        if not restore_original:
            data["virtual_machine_name"] = virtual_machine_name
            if datastore:
                if not isinstance(datastore, datastores.Datastore):
                    # if passed by datastore name
                    datastore_obj = datastores.Datastores(self._connection)
                    datastore = datastore_obj.get_by_name(datastore)
                data["datastore_id"] = datastore.data["id"]

        flags = {"restore_original": restore_original}
        affected_object = self._client.do_post(resource_uri, data, timeout, None, flags)[0]
        virtual_machines_obj = virtual_machines.VirtualMachines(self._connection)
        return virtual_machines_obj.get_by_id(affected_object["object_id"])

    def lock(self, timeout=-1):
        """Saves the specified backup to prevent it from expiring"""
        resource_uri = "{}/{}/lock".format(URL, self.data["id"])
        self._client.do_post(resource_uri, None, timeout)
        self.__refresh()

        return self

    def rename(self, new_name, timeout=-1):
        """Renames the specified backup
        Args:
            new_name: The new name for the backup.
            timeout: Time out for the request in seconds.

        Returns:
            object: Backup object.
        """

        resource_uri = "{}/{}/rename".format(URL, self.data["id"])
        data = {'backup_name': new_name}
        self._client.do_post(resource_uri, data, timeout)
        self.__refresh()
        return self

    def cancel(self, timeout=-1):
        """Cancels the specified running backup
        Args:
          timeout: Time out for the request in seconds.

        Returns:
          object: Backup object.
        """
        resource_uri = "{}/{}/cancel".format(URL, self.data["id"])
        self._client.do_post(resource_uri, None, timeout)
        self.__refresh()
        return self

    def copy(self, cluster=None, external_store_name=None, timeout=-1):
        """Copies the specified backup to another omnistack_cluster or external store
        Args:
            cluster: Destination OmnistackCluster object/name.
            external_store_name: The name of the external store.
            timeout: Time out for the request in seconds.

        Returns:
            object: Returns the new backup object.
        """

        resource_uri = "{}/{}/copy".format(URL, self.data["id"])
        data = {}
        if cluster:
            if not isinstance(cluster, omnistack_clusters.OmnistackCluster):
                # if passed name of the cluster
                clusters_obj = omnistack_clusters.OmnistackClusters(self._connection)
                cluster = clusters_obj.get_by_name(cluster)
            data['destination_id'] = cluster.data['id']

        if external_store_name:
            data['external_store_name'] = external_store_name

        affected_object = self._client.do_post(resource_uri, data, timeout)[0]
        return self._backups.get_by_id(affected_object["object_id"])

    def get_virtual_disk_partitions(self, virtual_disk):
        """Retrieves partition information for the virtual disk associated with the backup
        Args:
            virtual_disk: The name of the virtual hard disk for the virtual machine.

        Returns:
            dict: Returns dictionary containing partition information for the virtual disk associated.
        """

        resource_uri = "{}/{}/virtual_disk_partitions".format(URL, self.data["id"])
        data = {'virtual_disk': virtual_disk}

        return self._client.do_get(resource_uri, data)

    def get_virtual_disk_partition_files(self, virtual_disk, partition_number, file_path):
        """Retrieves the virtual hard disk files from the backup
        Args:
            virtual_disk: The name of the virtual hard disk for the virtual machine.
            partition_number: The partition number of the virtual disk associated with the backup.
            file_path: The path in the partition that has the file information you want. e.g. for root directory use "/".

        Returns:
            dict: Returns dictionary containing virtual hard disk files from the backup.
        """

        resource_uri = "{}/{}/virtual_disk_partition_files".format(URL, self.data["id"])
        data = {'virtual_disk': virtual_disk,
                'partition_number': partition_number,
                'file_path': file_path}

        return self._client.do_get(resource_uri, data)

    def restore_files(self, virtual_machine_id, paths, timeout=-1):
        """Restores files from specific partition

        Args:
           virtual_machine_id: The identification number of the virtual machine where you want to restore the files.
           paths: List of path to the files in this format: virtual_machine_disk_name/partition_number/path_to_file.

        Returns:
           None
        """
        resource_uri = "{}/{}/restore_files".format(URL, self.data["id"])
        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.9+json'}
        data = {"virtual_machine_id": virtual_machine_id,
                "paths": paths}

        self._client.do_post(resource_uri, data, timeout, custom_headers)
