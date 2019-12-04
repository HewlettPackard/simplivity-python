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

URL = '/omnistack_clusters'
DATA_FIELD = 'omnistack_clusters'


class OmnistackClusters(ResourceBase):
    """Implements features available for OmniStack cluster resources."""

    def __init__(self, connection):
        super(OmnistackClusters, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True, show_optional_fields=False):
        """Gets all omnistack clusters.

        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs.
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
              id: The unique identifier (UID) of the omnistack_clusters to return
                Accepts: Single value, comma-separated list
              name: The name of the omnistack_clusters to return
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              hypervisor_object_id: The unique identifier (UID) of the hypervisor associated
                with the objects to return
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              hypervisor_object_parent_id: The unique identifier (UID) of the hypervisor that
                contains the objects to return
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              hypervisor_object_parent_name: The name of the hypervisor that contains the objects
                to return
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              hypervisor_management_system_name: The name of the hypervisor associated with the
                omnistack_cluster
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              type: The type of omnistack_clusters to return
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              arbiter_address: The address of the Arbiter connected to the objects to return
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              arbiter_connected: An indicator to show if the omnistack_cluster is connected to Arbiter
                Valid values:
                True: Only returns omnistack_clusters connected to Arbiters that you identified
                  in arbiter_address
                False: Only returns omnistack_clusters not connected to Arbiters that you identified
                  in arbiter_address

        Returns:
          list: list of OmnistackCluster
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
        """Gets OmnistackCluster object from data.

        Args:
            data: OmnistackCluster data

        Returns:
            object: OmnistackCluster object.
        """

        return OmnistackCluster(self._connection, self._client, data)


class OmnistackCluster(object):
    """Implements features available for single OmniStack cluster resource."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
