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

    def get_time_zone_list(self):
        """Retrieves a list of all valid time zones"""

        resource_uri = "{}/time_zone_list".format(URL)
        return self._client.do_get(resource_uri)


class OmnistackCluster(object):
    """Implements features available for single OmniStack cluster resource."""

    OBJECT_TYPE = "omnistack_cluster"

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
        self._clusters = OmnistackClusters(self._connection)

    def get_connected_clusters(self):
        """Retrieves directly connected omnistack_clusters.

        Returns:
            list: List of omnistack_clusters objects.
        """
        method_url = "{}/{}/connected_clusters".format(URL, self.data["id"])
        connected_clusters = self._client.do_get(method_url).get("omnistack_clusters", [])

        clusters = [self._clusters.get_by_id(cluster["id"]) for cluster in connected_clusters]

        return clusters

    def get_throughput(self, destination_id=None, time_offset=0, range=43200):
        """Calculates the throughput between each pair of omnistack_clusters in the federation

        Args:
            destination_id : The unique identifier (UID) of the omnistack_clusters to return
            time_offset : A time offset in seconds (from now) or a datetime,
                        expressed in ISO-8601 form, based on Coordinated Universal Time (UTC) Default: 0
            range : A range in seconds (the duration from the specified point in time) Default: 43200

        Returns:
            dict: Dictionary of cluster_throughput object.
        """
        method_url = "{}/{}/throughput".format(URL, self.data["id"])
        filters = {'time_offset': time_offset, 'range': range}
        if (destination_id):
            filters['destination_id'] = destination_id

        return self._client.do_get(method_url, filters)

    def __refresh(self):
        """Updates the omnistack cluster data."""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self.data = self._client.do_get(resource_uri)[self.OBJECT_TYPE]

    def set_time_zone(self, time_zone, timeout=-1):
        """ Sets the time zone for a cluster.

        Args:
            time_zone: The time zone in case-sensitive region/locale format
                       for example, "America/New_York"
            timeout : Time out for the request in seconds.

        Returns:
            object: omnistack cluster object.
        """

        method_url = "{}/{}/set_time_zone".format(URL, self.data["id"])
        data = {"time_zone": time_zone}
        self._client.do_post(method_url, data, timeout)
        self.__refresh()
        return self

    def get_metrics(self, time_offset=0, range=43200, resolution='MINUTE'):
        """Retrieves throughput, IOPS, and latency data for cluster.

        Args:
            time_offset: A time offset in seconds (from now) or a datetime,
                        expressed in ISO-8601 form, based on Coordinated Universal Time (UTC) Default: 0
            range: A range in seconds (the duration from the specified point in time) Default: 43200
            resolution: The resolution (SECOND, MINUTE, HOUR, or DAY) Default: MINUTE

        Returns:
            dict: Dictionary of metrics object.
        """
        method_url = "{}/{}/metrics".format(URL, self.data["id"])
        filters = {'time_offset': time_offset, 'range': range, 'resolution': resolution}

        return self._client.do_get(method_url, filters)
