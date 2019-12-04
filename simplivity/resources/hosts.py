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

URL = '/hosts'
DATA_FIELD = 'hosts'


class Hosts(ResourceBase):
    """Implements features available for SimpliVity Host resources."""

    def __init__(self, connection):
        super(Hosts, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True, show_optional_fields=False):
        """Gets all hosts.

        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs.
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
              id: The unique identifier (UID) of the host
                Accepts: Single value, comma-separated list
              name: The name of the host
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              type: The type of host
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              model: The model of the host
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              version: The version of the host
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              hypervisor_management_system: The IP address of the Hypervisor Management System (HMS)
                associated with the host
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              hypervisor_management_system_name: The name of the Hypervisor Management System (HMS)
                associated with the host
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              hypervisor_object_id: The unique identifier (UID) of the hypervisor associated
                with the host
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              compute_cluster_name: The name of the compute cluster associated with the host
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              compute_cluster_hypervisor_object_id: The unique identifier (UID)
                of the Hypervisor Management System (HMS) for the associated compute cluster
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              management_ip: The IP address of the HPE OmniStack management module that
                runs on the host
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              storage_ip: The IP address of the HPE OmniStack storage module that runs on the host
                Accepts: Single value, comma-separated list, pattern using one or more
                asterisk characters as a wildcard
              federation_ip: The IP address of the federation
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              virtual_controller_name: The name of the Virtual Controller that runs on the host
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              compute_cluster_parent_name: The name of the hypervisor that contains the omnistack
                cluster that is associated with the instance
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              compute_cluster_parent_hypervisor_object_id: The unique identifier (UID) of the
                hypervisor that contains the omnistack_cluster that is associated with the instance
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              policy_enabled: An indicator to show the status of the backup policy for the host
                Valid values:
                True: The backup policy for the host is enabled.
                False: The backup policy for the host is disabled.
              current_feature_level_min: The minimum current feature level of the HPE OmniStack
                software running on the host
              current_feature_level_max: The maximum current feature level of the HPE OmniStack
                software running on the host
              potential_feature_level_min: The minimum potential feature level of the HPE OmniStack
                software running on the host
              potential_feature_level_max: The maximum potential feature level of the HPE OmniStack
                software running on the host
              upgrade_state: The state of the most recent HPE OmniStack software upgrade for this
                host (SUCCESS, FAIL, IN_PROGRESS, NOOP, UNKNOWN)
                Accepts: Single value, comma-separated list, pattern using one or more asterisk
                characters as a wildcard
              can_rollback: An indicator to show if the current HPE OmniStack software running on
                the host can roll back to the previous version
                Valid values:
                True: The current HPE OmniStack software for the host can roll back to the previous version.
                False: The current HPE OmniStack software for the host cannot roll back to the previous version.

        Returns:
          list: list of Host objects
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
        """Gets Host object from host data.

        Args:
            data: host data

        Returns:
            object: Host object.
        """
        return Host(self._connection, self._client, data)


class Host(object):
    """Implements features available for single Host resource."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
