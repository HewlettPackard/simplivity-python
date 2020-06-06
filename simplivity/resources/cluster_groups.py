###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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

URL = '/cluster_groups'
DATA_FIELD = 'cluster_groups'


class ClusterGroups(ResourceBase):
    """Implements features available for cluster group resources."""

    def __init__(self, connection):
        super(ClusterGroups, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True, show_optional_fields=False):
        """Gets all cluster groups.

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
        """Gets ClusterGroup object from data.

        Args:
            data: ClusterGroup data

        Returns:
            object: ClusterGroup object.
        """

        return ClusterGroup(self._connection, self._client, data)


class ClusterGroup(object):
    """Implements features available for single cluster group resource."""

    OBJECT_TYPE = 'cluster_group'

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
        self._cluster_groups = ClusterGroups(self._connection)

    def __refresh(self):
        """Updates the cluster_group data."""
        resource_object = self._cluster_groups.get_by_id(self.data["id"])
        self.data = resource_object.data

    def rename(self, name, timeout=-1):
        """Rename a cluster_group.

        Args:
            name: The name of the cluster group.
            timeout: Time out for the request in seconds.

        Returns:
        object: ClusterGroup object.
        """
        resource_uri = "{}/{}/rename".format(URL, self.data["id"])
        data = {"cluster_group_name": name}
        self._client.do_post(resource_uri, data, timeout)
        # The Response Class has an embedded affected_objects list; however
        # the list is not being populated for this POST operation.
        self.__refresh()

        return self
