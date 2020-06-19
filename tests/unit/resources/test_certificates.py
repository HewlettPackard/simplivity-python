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

import unittest
from unittest import mock

from simplivity.connection import Connection
from simplivity.resources import certificates
from simplivity import exceptions


class SecurityCertificatesTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection('127.0.0.1')
        self.connection._access_token = "123456789"
        self.certificates = certificates.Certificates(self.connection)

    @mock.patch.object(Connection, "get")
    def test_get_all_returns_resource_obj(self, mock_get):
        url = "{}?case=sensitive&limit=500&offset=0&order=descending&sort=name".format(certificates.URL)
        resource_data = [{
            "certificate": "-----BEGIN CERTIFICATE-----\nMIIEETCCALfslHOA==\n-----END CERTIFICATE-----",
            "hash": "701b27e9223654a697cf7052c71872016",
            "subject": "OU=Test,O=vc-123-12-12,ST=UNR,C=US,DC=local,DC=vsphere,CN=CA",
            "issuer": "OU=Test,O=vc-123-12-12,ST=UNR,C=US,DC=local,DC=vsphere,CN=CA",
            "serialno": "asdga2353456sfsh"}]
        mock_get.return_value = {certificates.DATA_FIELD: resource_data}

        objs = self.certificates.get_all()
        self.assertIsInstance(objs[0], certificates.Certificate)
        self.assertEqual(objs[0].data, resource_data[0])
        mock_get.assert_called_once_with(url)

    def test_get_by_name_not_found(self):
        cert_name = "cert1"

        with self.assertRaises(exceptions.HPESimpliVityMethodNotSupportedError) as error:
            self.certificates.get_by_name(cert_name)

        self.assertEqual(error.exception.msg, "Method get_by_name is not supported")

    def test_get_by_id_not_found(self):
        cert_id = "875623409753"

        with self.assertRaises(exceptions.HPESimpliVityMethodNotSupportedError) as error:
            self.certificates.get_by_id(cert_id)

        self.assertEqual(error.exception.msg, "Method get_by_id is not supported")


if __name__ == '__main__':
    unittest.main()
