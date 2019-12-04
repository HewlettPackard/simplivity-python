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

URL = '/datastores'
DATA_FIELD = 'datastores'


class Datastores(ResourceBase):
    """Implements features available for SimpliVity Datastore resources."""

    def __init__(self, connection):
        super(Datastores, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True, show_optional_fields=False):
        """Gets all datastores.

        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs.
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
              id: The unique identifier (UID) of the datastores to return
                Accepts: Single value, comma-separated list
              name: The name of the datastores to return
                Accepts: Single value, comma-separated list, pattern using one
                or more asterisk characters as a wildcard
              min_size: The minimum size (in bytes) of datastores to return
              max_size: The maximum size (in bytes) of datastores to return
              created_before: The latest creation time before the datastores to return were created,
                expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              created_after: The earliest creation time after the datastores to return were created,
                expressed in ISO-8601 form, based on Coordinated Universal Time (UTC)
              omnistack_cluster_id: The unique identifier (UID) of the omnistack_cluster that is
                associated with the instances to return
                Accepts: Single value, comma-separated list
              omnistack_cluster_name: The name of the omnistack_cluster that is associated with
                the instances to return
                Accepts: Single value, comma-separated list
              compute_cluster_parent_hypervisor_object_id: The unique identifier (UID) of the hypervisor
                that contains the omnistack_cluster that is associated with the instances to return
                Accepts: Single value, comma-separated list
              compute_cluster_parent_name: The name of the hypervisor that contains the omnistack
                cluster that is associated with the instances to return
                Accepts: Single value, comma-separated list
              hypervisor_management_system_name: The name of the Hypervisor Management System (HMS)
                associated with the datastore
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              policy_id: The unique identifier (UID) of the policy that is associated with the
                instances to return
                Accepts: Single value, comma-separated list
              policy_name: The name of the policy that is associated with the instances to return
                Accepts: Single value, comma-separated list
              hypervisor_object_id: The unique identifier (UID) of the hypervisor-based instance
                that is associated with the instances to return
                Accepts: Single value, comma-separated list
              mount_directory: A comma-separated list of fields to include in the returned objects
                Default: Returns all fields

        Returns:
          list: list of Datastore objects.
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
        """Gets Datastore object from data.

        Args:
            data: Datastore data

        Returns:
            object: Datastore object.
        """
        return Datastore(self._connection, self._client, data)


class Datastore(object):
    """Implements features available for single Datastore resource."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
