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
from simplivity import exceptions

"""Implements features available for certificate resource."""
URL = '/security/certificates'
DATA_FIELD = 'certificates'


class Certificates(ResourceBase):
    """Implements features for SimpliVity Certificates resources."""

    def __init__(self, connection):
        """Initialize Certificates class."""
        super(Certificates, self).__init__(connection)

    def get_all(self):
        """Get all SSL certificates from the HPE SimpliVity trust store"""
        return self._client.get_all(URL, members_field=DATA_FIELD)

    def get_by_data(self, data):
        """Gets Certificate object from data.

        Args:
            data: Certificate data

        Returns:
            object: Certificate object.
        """
        return Certificate(self._connection, self._client, data)

    def get_by_id(self, resource_id):
        """ Method not available on resource"""
        raise exceptions.HPESimpliVityMethodNotSupportedError("Method get_by_id is not supported")

    def get_by_name(self, name):
        """ Method not available on resource"""
        raise exceptions.HPESimpliVityMethodNotSupportedError("Method get_by_name is not supported")

    def add_certificate(self, certificate, timeout=-1):
        """Add a SSL certificate to the HPE SimpliVity trust store

        Args:
            certificate: Base64 encoded SSL certificate.
            timeout: Time out for the request in seconds.

        Returns:
            dict : Returns the certificate details.
        """

        data = {"certificate": certificate}
        return self._client.do_post(URL, data, timeout)


class Certificate(object):
    """Implements features available for single Certificate resource."""

    def __init__(self, connection, resource_client, data):
        self.data = data
        self._connection = connection
        self._client = resource_client
