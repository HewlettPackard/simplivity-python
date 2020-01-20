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

import unittest
import mock

from simplivity.connection import Connection
from simplivity import exceptions
from simplivity.resources.resource import ResourceClient, Pagination
from simplivity.resources.resource import PAGE_SIZE_NOT_SET


class ResourceStub():
    def __init__(self):
        self.data = None

    def get_by_data(self, data):
        self.data = data
        return self


class ResourceTest(unittest.TestCase):

    def setUp(self):
        self.Connection = Connection('127.0.0.1')
        resource_obj = ResourceStub()
        self.resource_client = ResourceClient(self.Connection, resource_obj)

    @mock.patch.object(Connection, "get")
    def test_get_all_called_once(self, mock_get):
        filter = {'name': 'test'}
        sort = 'name'
        optional_fields = "testfield,testfield1"
        fields = "field1,field2"
        mock_get.return_value = {'member_field': [{'name': 'testname', 'id': '1234567'}]}

        result = self.resource_client.get_all('/api/resource', 'member_field',
                                              filters=filter, sort=sort,
                                              show_optional_fields=optional_fields,
                                              fields=fields)

        url = '/api/resource?case=sensitive&fields={}&limit=500&name={}' \
              '&offset=0&order=descending&show_optional_fields={}' \
              '&sort={}'.format('field1%2Cfield2', filter["name"], 'testfield%2Ctestfield1', sort)

        self.assertIsInstance(result[0], ResourceStub)
        self.assertEqual({'name': 'testname', 'id': '1234567'}, result[0].data)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "get")
    def test_get_all_with_defaults(self, mock_get):
        self.resource_client.get_all('/api/resource')
        uri = '/api/resource?case=sensitive&limit=500&offset=0&order=descending&sort=name'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Connection, "get")
    def test_get_all_should_return_empty_list_when_response_has_no_items(self, mock_get):
        mock_get.return_value = {}
        result = self.resource_client.get_all('/api/resource')
        self.assertEqual(result, [])

    @mock.patch.object(Connection, "get")
    def test_get_all_with_pagination(self, mock_get):
        mock_get.return_value = {None: [1, 2, 3]}
        result = self.resource_client.get_all('/api/resource', pagination=True, page_size=10)
        self.assertIsInstance(result, Pagination)

    @mock.patch.object(Connection, "get")
    def test_get_all_with_paginatin_without_page_size(self, mock_get):
        with self.assertRaises(exceptions.HPESimpliVityException) as error:
            self.resource_client.get_all('/api/resource', pagination=True)
        self.assertEqual(error.exception.msg, PAGE_SIZE_NOT_SET)

    @mock.patch.object(Connection, "get")
    def test_get_call(self, mock_get):
        url = "/api/resource"
        self.resource_client.do_get(url)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(Connection, "post")
    def test_post_call(self, mock_post):
        url = "/api/resource"
        data = {"name": "name"}
        mock_post.return_value = None, {}
        self.resource_client.do_post(url, data, -1, None)
        mock_post.assert_called_once_with(url, data, custom_headers=None)

    @mock.patch.object(Connection, "post")
    @mock.patch.object(Connection, "get")
    def test_post_call_with_task(self, mock_get, mock_post):
        url = "/api/resource"
        data = {"name": "name"}
        affected_objects = ["1234567"]
        mock_post.return_value = {'id': '12345', 'state': 'INPROGRESS'}, {}
        mock_get.return_value = {'task': {'id': '12345', 'state': 'COMPLETED', 'affected_objects': affected_objects}}
        result = self.resource_client.do_post(url, data, -1, None)

        mock_post.assert_called_once_with(url, data, custom_headers=None)
        self.assertEqual(result, affected_objects)

    @mock.patch.object(Connection, "put")
    def test_put_call(self, mock_put):
        url = "/api/resource"
        data = {"name": "name"}
        mock_put.return_value = None, {}
        self.resource_client.do_put(url, data, -1, None)
        mock_put.assert_called_once_with(url, data, custom_headers=None)

    @mock.patch.object(Connection, "put")
    @mock.patch.object(Connection, "get")
    def test_put_call_with_task(self, mock_get, mock_put):
        url = "/api/resource"
        data = {"name": "name"}
        affected_objects = ["1234567"]
        mock_put.return_value = {'id': '12345', 'state': 'INPROGRESS'}, {}
        mock_get.return_value = {'task': {'id': '12345', 'state': 'COMPLETED', 'affected_objects': affected_objects}}
        result = self.resource_client.do_put(url, data, -1, None)

        mock_put.assert_called_once_with(url, data, custom_headers=None)
        self.assertEqual(result, affected_objects)


if __name__ == '__main__':
    unittest.main()
