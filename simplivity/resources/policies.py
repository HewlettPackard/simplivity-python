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

"""Implements operations for policies."""

from simplivity.resources.resource import ResourceBase
import simplivity.resources as resources

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


class Policy(object):
    """Implements features available for a single Policy resource."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client

    def get_vms(self):
        """Retrieves the virtual machines using this policy.

        Returns:
          list: List of vms.
        """
        method_url = "{}/{}/virtual_machines".format(URL, self.data["id"])
        vm_data = self._client.do_get(method_url).get("virtual_machines", [])

        vms_obj = resources.virtual_machines.VirtualMachines(self._connection)
        vms = []

        for vm in vm_data:
            vms.append(vms_obj.get_by_id(vm["id"]))

        return vms
