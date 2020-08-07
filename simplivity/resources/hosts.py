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

    OBJECT_TYPE = 'host'

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
        self._hosts = Hosts(self._connection)

    def remove(self, force=False, timeout=-1):
        """Removes the specified host from the federation.

        Args:
          force: An indicator that specifies if the host should be removed forcefully or not.
            Valid values:
              True: Forces the removal of the host even if active virtual machines are
                    present and if the host is not HA-compliant. This may cause data loss.
              False: Returns an error if there are any virtual machines on the host or if the host is not HA-compliant.
        """
        http_headers = {"Content-type": 'application/vnd.simplivity.v1.9+json'}

        method_url = "{}/{}/remove_from_federation".format(URL, self.data["id"])
        data = {"force": force}

        self._client.do_post(method_url, data, timeout, http_headers)
        self.data = None

    def get_hardware(self):
        """Retrieves the hardware information for the host"""
        resource_uri = "{}/{}/hardware".format(URL, self.data["id"])
        return self._client.do_get(resource_uri)

    def get_virtual_controller_shutdown_status(self):
        """Retrieves the shutdown status of the Virtual Controller"""
        resource_uri = "{}/{}/virtual_controller_shutdown_status".format(URL, self.data["id"])
        status = self._client.do_get(resource_uri)
        return status['shutdown_status']['status']

    def shutdown_virtual_controller(self, ha_wait=True, timeout=-1):
        """Shuts down the Virtual Controller safely (by reaching HA compliance) or by force.

        Args:
          ha_wait: An indicator to show if the user wants to shut down the Virtual Controller safely or forcefully.
            Valid values:
              True: Virtual Controller waits for the virtual machines to reach HA compliance before shutting down.
              False: Virtual Controller forced to shut down without waiting for HA compliance.
          timeout: Time out for the request in seconds.

        Returns:
            status: Possible values are 'SUCCESS', 'FAILURE', 'UNKNOWN', 'IN_PROGRESS'.
        """
        method_url = "{}/{}/shutdown_virtual_controller".format(URL, self.data["id"])
        data = {"ha_wait": ha_wait}

        status = self._client.do_post(method_url, data, timeout)
        return status['shutdown_status']['status']

    def cancel_virtual_controller_shutdown(self, timeout=-1):
        """Cancels the virtual controller shutdown.

        Args:
          timeout: Time out for the request in seconds.

        Returns:
          status: Possible values are 'SUCCESS', 'FAILURE', 'UNKNOWN', 'IN_PROGRESS'.
        """
        resource_uri = "{}/{}/cancel_virtual_controller_shutdown".format(URL, self.data["id"])
        status = self._client.do_post(resource_uri, None, timeout)
        return status['cancellation_status']['status']

    def get_capacity(self, fields=None, time_offset=0, range=43200, resolution="MINUTE"):
        """Gets host capacity.

        Args:
          fields: Comma-separated list of fields to include in the returned objects.
          time_offset: A time offset in seconds (from now) or a datetime, expressed in ISO-8601 form,
                       based on Coordinated Universal Time (UTC).
          range: A range in seconds (the duration from the specified point in time).
          resolution: The resolution (SECOND, MINUTE, HOUR, or DAY).

        Returns:
          dict: Dictionary of the capacity details.
        """
        resource_uri = "{}/{}/capacity".format(URL, self.data["id"])
        filters = {'time_offset': time_offset, 'range': range, 'resolution': resolution}

        if fields:
            filters["fields"] = fields

        return self._client.do_get(resource_uri, filters)

    def get_metrics(self, time_offset=0, range=43200, resolution="MINUTE"):
        """Retrieves throughput, IOPS, and latency data for the host.

        Args:
          time_offset: A time offset in seconds (from now) or a datetime, expressed in ISO-8601 form,
                       based on Coordinated Universal Time (UTC).
          range: A range in seconds (the duration from the specified point in time).
          resolution: The resolution (SECOND, MINUTE, HOUR, or DAY).

        Returns:
          dict: Dictionary of the metrics details.
        """
        resource_uri = "{}/{}/metrics".format(URL, self.data["id"])
        filters = {'time_offset': time_offset, 'range': range, 'resolution': resolution}

        return self._client.do_get(resource_uri, filters)
