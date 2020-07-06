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
from simplivity.resources import omnistack_clusters
from simplivity.resources import policies

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

    def create(self, datastore_name, cluster, policy, size=0, timeout=-1):
        """Creates a new datastore.

        Args:
            datastore_name: The name of the new datastore created from this action.
            cluster: Destination OmnistackCluster object/name.
            policy: Object/name of the policy to assocaited with the new datastore.
            size: The size in bytes of the new datastore.
            timeout: Time out for the request in seconds.

        Returns:
            object: Datastore object.
        """
        method_url = "{}".format(URL)

        if not isinstance(cluster, omnistack_clusters.OmnistackCluster):
            # if passed name of the cluster
            clusters_obj = omnistack_clusters.OmnistackClusters(self._connection)
            cluster = clusters_obj.get_by_name(cluster)

        if not isinstance(policy, policies.Policy):
            # if passed name of the policy
            policies_obj = policies.Policies(self._connection)
            policy = policies_obj.get_by_name(policy)

        data = {
            "name": datastore_name,
            "omnistack_cluster_id": cluster.data['id'],
            "policy_id": policy.data['id'],
            "size": size
        }

        out = self._client.do_post(method_url, data, timeout, None)
        return self.get_by_id(out[0]["object_id"])


class Datastore(object):
    """Implements features available for single Datastore resource."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client

    def __refresh(self):
        """Updates the datastore data."""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self.data = self._client.do_get(resource_uri)['datastore']

    def delete(self, timeout=-1):
        """Deletes a datastore."""
        resource_uri = "{}/{}".format(URL, self.data["id"])
        self._client.do_delete(resource_uri, timeout, None)
        self.data = None

    def resize(self, size, timeout=-1):
        """Resizes a datastore.

        Args:
            size: The size in bytes.
            timeout: Time out for the request in seconds.

        Returns:
            object: Datastore object.

        """
        resource_uri = "{}/{}/resize".format(URL, self.data["id"])
        data = {"size": size}
        out = self._client.do_post(resource_uri, data, timeout, None)
        datastore = Datastores(self._connection)
        datastore_obj = datastore.get_by_id(out[0]["object_id"])
        self.data = datastore_obj.data

        return self

    def set_policy(self, policy, timeout=-1):
        """Sets the backup policy for a datastore.

        Args:
            policy: Policy object/name
            timeout: Time out for the request in seconds.

        Returns:
            object: Datastore object.

        """
        resource_uri = "{}/{}/set_policy".format(URL, self.data["id"])
        if not isinstance(policy, policies.Policy):
            # if passed name of the policy
            policy = policies.Policies(self._connection).get_by_name(policy)

        data = {"policy_id": policy.data['id']}
        self._client.do_post(resource_uri, data, timeout, None)
        self.__refresh()

        return self

    def standard_hosts(self):
        """Gets the standard hosts that can share a datastore.

        Returns:
            list: List of standard hosts objects.

        """
        resource_uri = "{}/{}/standard_hosts".format(URL, self.data["id"])
        return self._client.do_get(resource_uri)

    def share(self, host_name, timeout=-1):
        """Share a datastore.

        Args:
          host_name: The name of the standard host that you want sharing a datastore.
          timeout: Time out for the request in seconds.

        Returns:
          object: Datastore object.
        """

        resource_uri = "{}/{}/share".format(URL, self.data["id"])
        data = {"host_name": host_name}
        self._client.do_post(resource_uri, data, timeout)
        self.__refresh()

        return self

    def unshare(self, host_name, timeout=-1):
        """Stop sharing a datastore.

        Args:
          host_name: The name of the standard host that needs to stop sharing a datastore.
          timeout: Time out for the request in seconds.

        Returns:
          object: Datastore object.
        """

        resource_uri = "{}/{}/unshare".format(URL, self.data["id"])
        data = {"host_name": host_name}
        self._client.do_post(resource_uri, data, timeout)
        self.__refresh()

        return self
