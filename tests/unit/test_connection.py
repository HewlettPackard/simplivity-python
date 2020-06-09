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

import json
import ssl
import unittest
from http.client import HTTPException, HTTPSConnection
from unittest.mock import ANY, Mock, call, patch

from simplivity.connection import Connection
from simplivity.exceptions import HPESimpliVityException


class ConnectionTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = Connection(self.host)
        self.connection._access_token = "123456789"

        self.new_content_type = {
            'Content-type': 'application/vnd.simplivity.v1.7+json'
        }
        self.default_headers = {'Content-type': 'application/vnd.simplivity.v1.8+json',
                                'Authorization': 'Bearer 123456789',
                                'Accept': 'application/json'}

        self.updated_headers = self.default_headers.copy()
        self.updated_headers.update(self.new_content_type)

        self.request_body = {"request body": "content"}
        self.response_body = {"response body": "content"}

        self.error_response_body = {"message": "this is an error message"}

        self.dumped_request_body = json.dumps(self.request_body.copy())
        self.expected_response_body = self.response_body.copy()

    def __make_http_response(self, status, response_body=None):
        if response_body is None:
            response_body = self.response_body

        mock_response = Mock(status=status)
        mock_response.read.return_value = json.dumps(response_body).encode('utf-8')
        return mock_response

    def __create_fake_mapped_file(self):
        mock_mapped_file = Mock()
        mock_mapped_file.tell.side_effect = [0, 1048576, 2097152, 2621440]  # 0, 1MB, 2MB 2.5MB
        mock_mapped_file.size.return_value = 2621440  # 2.5MB
        mock_mapped_file.read.side_effect = ['data chunck 1', 'data chunck 2', 'data chunck 3']
        return mock_mapped_file

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_when_response_is_task(self, mock_response, mock_request):
        mock_request.return_value = {}

        fake_task = {"task": {"state": "COMPLETED"}}

        response = Mock(status=202)
        response.read.return_value = json.dumps(fake_task).encode('utf-8')
        response.getheader.return_value = ''
        mock_response.return_value = response

        task, body = self.connection.post('/path', self.request_body)
        self.assertEqual(task, fake_task)
        self.assertEqual(body, fake_task)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_when_response_is_not_a_task(self, mock_response, mock_request):
        mock_request.return_value = {}

        response = Mock(status=202)
        response.read.return_value = json.dumps(self.response_body).encode('utf-8')
        response.getheader.return_value = ''
        mock_response.return_value = response

        task, body = self.connection.post('/path', self.request_body)

        self.assertEqual(task, None)
        self.assertEqual(body, self.response_body)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_get_when_status_is_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        body = self.connection.get('/path')

        self.assertEqual(body, self.response_body)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_do_rest_call_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.post('/path', self.request_body)

        mock_request.assert_called_once_with('POST', "https://{}/api/path".format(self.host),
                                             self.dumped_request_body, self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_send_updated_headers_when_headers_provided(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.post('/path', self.request_body, custom_headers=self.new_content_type)

        expected_calls = [call('POST', ANY, ANY, self.updated_headers)]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_get_should_raise_exception_when_status_internal_error(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(
            status=401,
            response_body=self.error_response_body
        )

        with self.assertRaises(HPESimpliVityException) as context:
            self.connection.get('/path')

        self.assertTrue(self.error_response_body.get('message') in context.exception.msg)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_raise_exception_when_status_internal_error(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(
            status=401,
            response_body=self.error_response_body
        )

        with self.assertRaises(HPESimpliVityException) as context:
            self.connection.post('/path', self.request_body)

        self.assertTrue(self.error_response_body.get('message') in context.exception.msg)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_raise_exception_when_status_forbidden(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(
            status=403,
            response_body=self.error_response_body
        )

        with self.assertRaises(HPESimpliVityException) as context:
            self.connection.post('/path', self.request_body)

        self.assertTrue(self.error_response_body.get('message') in context.exception.msg)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_raise_exception_when_status_not_found(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(
            status=404,
            response_body=self.error_response_body
        )

        with self.assertRaises(HPESimpliVityException) as context:
            self.connection.post('/path', self.request_body)

        self.assertTrue(self.error_response_body.get('message') in context.exception.msg)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_do_rest_call_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.put('/path', self.request_body)

        mock_request.assert_called_once_with('PUT',
                                             'https://{}/api/path'.format(self.host),
                                             self.dumped_request_body, self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_return_body_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        result = self.connection.put('/path', self.response_body, custom_headers=self.new_content_type)

        expected_result = (None, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_do_rest_calls_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.delete('/path')

        mock_request.assert_called_once_with('DELETE',
                                             'https://{}/api/path'.format(self.host),
                                             json.dumps({}), self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_return_body_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        result = self.connection.delete('/path',
                                        custom_headers=self.new_content_type)

        expected_result = (None, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(Connection, 'do_http')
    def test_task_in_response_body(self, mock_do_http):
        mockedResponse = type('mockResponse', (), {'status': 200})()
        mockedTaskBody = {'task': {'state': 'INPROGRESS'}}
        mock_do_http.return_value = (mockedResponse, mockedTaskBody)

        (testTask, testBody) = self.connection._Connection__do_rest_call('PUT', '/path', '{ "body": "test" }', None)

        self.assertEqual(mockedTaskBody, testTask)
        self.assertEqual(mockedTaskBody, testBody)

    @patch.object(Connection, 'get_connection')
    def test_do_http_with_timeout_error(self, mock_get_connection):

        mock_conn = mock_get_connection.return_value = Mock()
        mock_response = Mock()
        mock_conn.getresponse.side_effect = [HTTPException('timed out'), mock_response]

        with self.assertRaises(HPESimpliVityException) as context:
            resp, body = self.connection.do_http('POST', '/rest/test', 'body')

        self.assertTrue('timed out' in context.exception.msg)

    def test_do_http_without_access_token(self):
        self.connection._access_token = None
        with self.assertRaises(HPESimpliVityException) as context:
            resp, body = self.connection.do_http('POST', '/rest/test', 'body')
        self.assertTrue('please login' in context.exception.msg)

    @patch.object(Connection, 'do_http')
    def test_login(self, mock_post):
        mock_post.return_value = (None, {'access_token': '1234567'})

        self.connection.login('username', 'password')

        self.assertEqual(self.connection._access_token, '1234567')

    @patch.object(Connection, 'do_http')
    def test_login_with_unexpected_body(self, mock_post):
        mock_post.return_value = (None, {})

        with self.assertRaises(HPESimpliVityException) as context:
            self.connection.login('username', 'password')

        self.assertTrue('Invalid credentials' in context.exception.msg)

    @patch.object(Connection, 'login')
    @patch.object(Connection, 'get_connection')
    def test_login_again_if_token_expired(self, mock_connection, mock_login):
        mock_invalid_token_response = self.__make_http_response(
            status=401,
            response_body={'error': 'invalid_token'}
        )
        mock_retry_request_response = self.__make_http_response(status=200)

        mock_conn = mock_connection.return_value = Mock()
        mock_conn.getresponse.side_effect = [mock_invalid_token_response, mock_retry_request_response]

        self.connection._username = 'username'
        self.connection._password = 'password'

        resp, body = self.connection.do_http('POST', '/rest/test', 'body')
        mock_login.assert_called_once_with('username', 'password')

        self.assertEqual(body, self.expected_response_body)

    def test_logout(self):
        self.connection.logout()

        self.assertIsNone(self.connection._access_token)

    def test_get_connection_ssl_trust_all(self):

        conn = self.connection.get_connection()

        self.assertEqual(conn.host, '127.0.0.1')
        self.assertEqual(conn.port, 443)
        self.assertEqual(conn._context.protocol, ssl.PROTOCOL_TLSv1_2)


if __name__ == '__main__':
    unittest.main()
