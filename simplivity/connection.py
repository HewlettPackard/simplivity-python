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

"""This module maintains communication with SimplVity."""

import http.client
from base64 import b64encode

import json
import logging
import ssl
import urllib
import traceback

from simplivity import exceptions

logger = logging.getLogger(__name__)


class Connection(object):
    """Helps to make connection with the OVC and do rest calls."""

    def __init__(self, ovc_ip, ssl_bundle=False, timeout=None):
        """Initialize Connection class"""
        self._ovc_ip = ovc_ip
        self._timeout = timeout
        self._ssl_trusted_bundle = ssl_bundle
        self._ssl_trust_all = False if ssl_bundle else True
        self._username = None
        self._password = None
        self._access_token = None

        self._headers = {'Accept': 'application/vnd.simplivity.v1+json'}
        self._base_url = "https://{}/api".format(ovc_ip)
        self.__connection = None

    def do_http(self, method, path, body, custom_headers=None, login=False):
        """Makes http calls.

        Args:
            method: HTTP methods (GET, POST, PUT, DELETE).
            path: URL
            body: Request body.
            custom_headers: Custom headers to update/append default headers.
            login: True if the call is for login and get the token.

        Returns:
            tuple: Tuple with two members (HTTP response object and the response body in json).
        """
        http_headers = self._headers.copy()
        path = "{}{}".format(self._base_url, path)

        if login:
            user_pass = b64encode(b"simplivity:").decode("ascii")
            http_headers.update({'Content-type': 'application/x-www-form-urlencoded',
                                 'Authorization': 'Basic %s' % user_pass})
        else:
            if not self._access_token:
                raise exceptions.HPESimpliVityException("There is no active session, please login")

            http_headers['Content-type'] = 'application/vnd.simplivity.v1.8+json'
            http_headers['Authorization'] = "Bearer " + self._access_token

        # Updates default headers with the custom headers
        if custom_headers:
            http_headers.update(custom_headers)

        try:
            if not self.__connection:
                self.__connection = self.get_connection()
            self.__connection.request(method, path, body, http_headers)
            resp = self.__connection.getresponse()
            response = resp.read()
            body = json.loads(response.decode('utf-8'))
        except http.client.HTTPException:
            raise exceptions.HPESimpliVityException(traceback.format_exc())

        # Updates token if expired
        if 'error' in body and body['error'] == 'invalid_token':
            self.login(self._username, self._password)
            self.do_http(method, path, body, custom_headers)

        return resp, body

    def get_connection(self):
        """Makes connection with the OVC.

        Returns:
          HTTPSConnection object
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if self._ssl_trust_all is False:
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(self._ssl_trusted_bundle)
            conn = http.client.HTTPSConnection(self._ovc_ip,
                                               context=context,
                                               timeout=self._timeout)
        else:
            context.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(self._ovc_ip,
                                               context=context,
                                               timeout=self._timeout)
        return conn

    def get(self, url):
        """Calls get http method.

        Args:
            url: Resource URL

        Returns:
            tuple: Tuple with two members (HTTP response object and the response body in json).

        Raises:
            HPESimpliVityException: if the response status is 400 and above
        """
        resp, body = self.do_http('GET', url, '')
        if resp.status >= 400:
            raise exceptions.HPESimpliVityException(body)

        return body

    def post(self, uri, body, custom_headers=None):
        """Calls post http method.

        Args:
            uri: Resource URI.
            body: Request body.
            custom_headers: Custome headers to update/append default headers.

        Returns:
            dict: Response body
        """

        return self.__do_rest_call('POST', uri, body, custom_headers=custom_headers)

    def put(self, uri, body, custom_headers=None):
        """Calls put http method.

        Args:
            uri: Resource URI.
            body: Request body.
            custom_headers: Custome headers to update/append default headers.

        Returns:
            tuple: Tuple with two members (HTTP response object and the response body in json).
        """
        return self.__do_rest_call('PUT', uri, body, custom_headers=custom_headers)

    def delete(self, uri, custom_headers=None):
        """Calls delete http method.

        Args:
            uri: Resource URI.
            custom_headers: Custom headers to appened/update default headers.

        Returns:
            tuple: Tuple with two members (HTTP response object and the response body in json).
        """
        return self.__do_rest_call('DELETE', uri, {}, custom_headers=custom_headers)

    def __body_content_is_task(self, body):
        """Check to find task in response body

        Args:
            body: Response body of a rest call

        Returns:
            boolean: Returns True if the body is task data or False
        """
        return isinstance(body, dict) and 'task' in body

    def __do_rest_call(self, http_method, url, body, custom_headers):
        """Calls do_http method and handles the http status code.

        Args:
            http_method: HTTP method (GET, POST, PUT and DELETE)
            url: Resource URL
            body: Request body
            custom_headers: Headers to appened/update default headers

        Returns:
            tuple: A tuple of two elements (task and response body)

        Raises:
            HPESimpliVityException: if the response status code is 401/403/404
        """
        resp, body = self.do_http(method=http_method,
                                  path=url,
                                  body=json.dumps(body),
                                  custom_headers=custom_headers)

        if resp.status in [400, 401, 403, 404]:
            raise exceptions.HPESimpliVityException(body)

        if self.__body_content_is_task(body):
            return body, body

        return None, body

    def login(self, username, password):
        """Login using OVC username and password.

        Args:
            username: OVC username
            password: OVC password

        Returns:
            boolean: Returns True if login is successfull.
        """
        login_url = "/oauth/token"
        data = {'grant_type': 'password',
                'username': username,
                'password': password}

        resp, body = self.do_http('POST', login_url, body=urllib.parse.urlencode(data), login=True)

        try:
            self._access_token = body["access_token"]
            logger.info('Logged in successfully')
        except KeyError:
            raise exceptions.HPESimpliVityAuthenticationError("Invalid credentials")

        # Save the username and password for refreshing the connection
        self._username = username
        self._password = password

        return True

    def logout(self):
        """Removes the access token.

        Returns:
            boolean: Returns True
        """
        self._access_token = None
        logger.info('Logged out successfully')

        return True
