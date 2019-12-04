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

from simplivity.resources.resource import ResourceBase

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


class Backup(object):
    """Implements features available for a single Backup resources."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
