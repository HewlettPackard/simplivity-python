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

"""Module to define SimpliVity exception classes."""

import logging

logger = logging.getLogger(__name__)


class HPESimpliVityException(Exception):
    """
    SimpliVity base Exception.

    Attributes:
       msg (str): Exception message.
       response (dict): SimpliVity rest response.
   """

    def __init__(self, data, error=None):
        self.msg = None
        self.response = None

        if isinstance(data, str):
            self.msg = data
        else:
            self.response = data

            if data and isinstance(data, dict):
                self.msg = data.get('message')

        if self.response:
            Exception.__init__(self, self.msg, self.response)
        else:
            Exception.__init__(self, self.msg)


class HPESimpliVityTaskError(HPESimpliVityException):
    """
    SimpliVity Task Error Exception.

    Attributes:
       msg (str): Exception message.
       error_code (str): A code which uniquely identifies the specific error.
    """

    def __init__(self, msg, error_code=None):
        super(HPESimpliVityTaskError, self).__init__(msg)
        self.error_code = error_code


class HPESimpliVityTimeout(HPESimpliVityException):
    """
    SimpliVity Timeout Exception.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPESimpliVityResourceNotFound(HPESimpliVityException):
    """
    SimpliVity Resource Not Found Exception.
    The exception is raised when an associated resource was not found.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPESimpliVityAuthenticationError(HPESimpliVityException):
    """
    SimpliVity Authentication Exception.
    The exception is raised when the credentials supplied is not valid.

    Attributes:
       msg (str): Exception message.
    """
    pass
