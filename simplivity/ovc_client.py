####
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

"""
This module implements a common client for HPE SimpliVity resources.
"""
import json
import os

from simplivity.connection import Connection
from simplivity import exceptions

from simplivity.resources.virtual_machines import VirtualMachines
from simplivity.resources.policies import Policies
from simplivity.resources.datastores import Datastores
from simplivity.resources.omnistack_clusters import OmnistackClusters
from simplivity.resources.backups import Backups
from simplivity.resources.hosts import Hosts


class OVC(object):
    """Client class for all the resources."""

    def __init__(self, config):
        """Initialize OVC class."""
        self.__connection = Connection(config["ip"], config.get('ssl_certificate', False), config.get('timeout'))
        if config.get("credentials"):
            username = config["credentials"].get("username")
            password = config["credentials"].get("password")
            self.__connection.login(username, password)
        else:
            exceptions.HPESimpliVityException("Credentials not provided")

        self.__virtual_machines = None
        self.__policies = None
        self.__datastores = None
        self.__omnistack_clusters = None
        self.__backups = None
        self.__hosts = None

    @classmethod
    def from_json_file(cls, file_name):
        """
        Construct OVC client using a json file.

        Args:
            file_name: json full path.

        Returns:
            OVC object
        """
        with open(file_name) as json_data:
            config = json.load(json_data)

        return cls(config)

    @classmethod
    def from_environment_variables(cls):
        """
        Construct OVC Client using environment variables.

        Returns:
            OVC object
        """
        ip = os.environ.get('SIMPLIVITYSDK_OVC_IP', '')
        username = os.environ.get('SIMPLIVITYSDK_USERNAME', '')
        password = os.environ.get('SIMPLIVITYSDK_PASSWORD', '')
        ssl_certificate = os.environ.get('SIMPLIVITYSDK_SSL_CERTIFICATE', '')
        timeout = os.environ.get('SIMPLIVITYSDK_CONNECTION_TIMEOUT')

        if not ip or not username or not password:
            raise exceptions.SimplivityExceptions("Make sure you have set mandatory env variables \
            (SIMPLIVITYSDK_OVC_IP, SIMPLIVITYSDK_USERNAME, SIMPLIVITYSDK_PASSWORD)")

        config = dict(ip=ip,
                      ssl_certificate=ssl_certificate,
                      credentials=dict(username=username, password=password),
                      timeout=timeout)

        return cls(config)

    @property
    def connection(self):
        """
        Gets the underlying OVC connection used by the OVC client.

        Returns:
            Connection object
        """
        return self.__connection

    @property
    def virtual_machines(self):
        """
        Gets the Virtual Machines client.

        Returns:
            VirtualMachines object
        """
        if not self.__virtual_machines:
            self.__virtual_machines = VirtualMachines(self.__connection)
        return self.__virtual_machines

    @property
    def policies(self):
        """
        Gets the Policies client.

        Returns:
            Policies object
        """
        if not self.__policies:
            self.__policies = Policies(self.__connection)
        return self.__policies

    @property
    def datastores(self):
        """
        Gets the Datastores client.

        Returns:
            Datastores object
        """
        if not self.__datastores:
            self.__datastores = Datastores(self.__connection)
        return self.__datastores

    @property
    def omnistack_clusters(self):
        """
        Gets the Omnistack clusters client.

        Returns:
            OmnistackClusters object
        """
        if not self.__omnistack_clusters:
            self.__omnistack_clusters = OmnistackClusters(self.__connection)
        return self.__omnistack_clusters

    @property
    def backups(self):
        """
        Gets the Backups client.

        Returns:
            Backups object
        """
        if not self.__backups:
            self.__backups = Backups(self.__connection)
        return self.__backups

    @property
    def hosts(self):
        """
        Gets the Hosts resource client.

        Returns:
            Hosts object
        """
        if not self.__hosts:
            self.__hosts = Hosts(self.__connection)
        return self.__hosts
