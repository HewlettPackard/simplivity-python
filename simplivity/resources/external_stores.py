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

URL = '/external_stores'
DATA_FIELD = 'external_stores'


class ExternalStores(ResourceBase):
    """Implements features available for SimpliVity External store resources."""

    def __init__(self, connection):
        super(ExternalStores, self).__init__(connection)

    def get_all(self, pagination=False, page_size=0, limit=500, offset=0,
                sort=None, order='descending', filters=None, fields=None,
                case_sensitive=True):
        """
        Get all external stores
        Args:
            pagination: True if need pagination
            page_size: Size of the page (Required when pagination is on)
            limit: A positive integer that represents the maximum number of results to return
            offset: A positive integer that directs the service to start returning
              the <offset value> instance, up to the limit.
            sort: The name of the field where the sort occurs
            order: The sort order preference. Valid values: ascending or descending.
            filters: Dictionary with filter values. Example: {'name': 'name'}
                name: The name of the external_stores to return.
                    Accepts: Single value, comma-separated list, pattern using one or more asterisk characters as a wildcard.
                omnistack_cluster_id: The name of the omnistack_cluster that is associated with the instances to return
                cluster_group_id:The unique identifiers (UIDs) of the cluster_groups associated with the external stores to return
                    Accepts: Single value, comma-separated list
                management_ip: The IP address of the external store
                    Accepts: Single value, comma-separated list, pattern using one or more asterisk characters as a wildcard
                type: The type of external store
                    Default: StoreOnceOnPrem

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
        """Gets ExternalStore object from data.

        Args:
            data: ExternalStore data

        Returns:
            object: ExternalStore object.
        """

        return ExternalStore(self._connection, self._client, data)

    def register_external_store(self, management_ip, name, cluster, username, password, management_port=9387,
                                storage_port=9388, external_store_type='StoreOnceOnPrem', timeout=-1):
        """ Register the external store.
        Args:
            management_ip: The IP address of the external store
            name: The name of the external_store
            cluster: Destination OmnistackCluster object/name.
            username: The client name of the external store
            password: The client password of the external store
            management_port: The management IP port of the external store. Default: 9387
            storage_port: The storage IP port of the external store. Default: 9388
            external_store_type: The type of external store. Default: StoreOnceOnPrem
            timeout: Time out for the request in seconds.

        Returns:
            object: External store object.
        """

        data = {'management_ip': management_ip, 'management_port': management_port, 'name': name,
                'username': username, 'password': password, 'storage_port': storage_port,
                'type': external_store_type}

        if not isinstance(cluster, omnistack_clusters.OmnistackCluster):
            # if passed name of the cluster
            clusters_obj = omnistack_clusters.OmnistackClusters(self._connection)
            cluster = clusters_obj.get_by_name(cluster)

        data['omnistack_cluster_id'] = cluster.data['id']
        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.11+json'}
        self._client.do_post(URL, data, timeout, custom_headers)

        return self.get_by_name(name)

    def update_credentials(self, name, username, password, management_ip=None, timeout=-1):
        """Update the IP address or credentials that HPE SimpliVity uses to access the external stores

         Args:
            name: The name of the external_store
            username: The client name of the external store
            password: The client password of the external store
            management_ip: The IP address of the external store
            timeout: Time out for the request in seconds.

        Returns:
            object: External store object.
        """

        resource_uri = "{}/update_credentials".format(URL)
        data = {'name': name, 'username': username, 'password': password}
        if management_ip:
            data['management_ip'] = management_ip

        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.15+json'}
        self._client.do_post(resource_uri, data, timeout, custom_headers)


class ExternalStore(object):
    """Implements features available for a single External store resources."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client

    def unregister_external_store(self, cluster, timeout=-1):
        """ Removes the external store as a backup destination for the cluster.
        Backups remain on the external store,but they can no longer be managed by HPE SimpliVity.
        Args:
            cluster: Destination OmnistackCluster object/name.
            timeout: Time out for the request in seconds.

        Returns:
            None
        """

        resource_uri = "{}/unregister".format(URL)
        data = {'name': self.data["name"]}
        if not isinstance(cluster, omnistack_clusters.OmnistackCluster):
            # if passed name of the cluster
            clusters_obj = omnistack_clusters.OmnistackClusters(self._connection)
            cluster = clusters_obj.get_by_name(cluster)

        data['omnistack_cluster_id'] = cluster.data['id']
        custom_headers = {'Content-type': 'application/vnd.simplivity.v1.15+json'}
        self._client.do_post(resource_uri, data, timeout, custom_headers)
