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

"""Implements operations for task."""

import logging
import time

from simplivity import exceptions

TASK_PENDING_STATES = ['IN_PROGRESS']
TASK_ERROR_STATES = ['ERROR']
TASK_COMPLETED_STATES = ['COMPLETED']

MSG_TIMEOUT = 'Waited %s seconds for task to complete, aborting'
MSG_INVALID_TASK = 'Invalid task was provided'


UNLIMITED_TIMEOUT = -1
URL = '/tasks'

logger = logging.getLogger(__name__)


class Task(object):
    """Implements operations for task."""

    def __init__(self, con, data):
        """Initializes Task with connection and data."""
        self._connection = con
        if 'task' in data:
            self.data = data["task"]
        else:
            self.data = data

        self.state = self.data["state"]

    @staticmethod
    def get_current_seconds():
        """Returns current time."""
        return int(time.time())

    def wait_for_task(self, timeout=-1):
        """Wait for task execution and return affected resources.

        Args:
            timeout: timeout in seconds

        Returns:
            list: Affected resources when creating or updating
        """
        self.__wait_task_completion(timeout)

        self.update_status()

        logger.debug("Waiting for task. Task state: " + str(self.data.get('state')))

        return self.get_affected_resources()

    def __wait_task_completion(self, timeout):
        """Wait for task completion.

        Args:
          timeout: timeout in seconds
        """
        if not self.data:
            raise exceptions.HPESimpliVityUnknownType(MSG_INVALID_TASK)

        logger.debug('Waiting for task completion...')

        # gets current cpu second for timeout
        start_time = self.get_current_seconds()
        # connection_failure_control = dict(last_success=self.get_current_seconds())

        i = 0
        while self.is_task_running():
            # wait 1 to 10 seconds
            # the value increases to avoid flooding server with requests
            i = i + 1 if i < 10 else 10

            logger.debug("Waiting for task. Task state: " + str(self.data.get('state')))

            time.sleep(i)
            if (timeout != UNLIMITED_TIMEOUT) and (start_time + timeout < self.get_current_seconds()):
                raise exceptions.HPESimpliVityTimeout(MSG_TIMEOUT % str(timeout))

    def is_task_running(self):
        """
        Check if a task is running according to: TASK_PENDING_STATES

        Returns:
            True when in TASK_PENDING_STATES; False when not.
        """
        self.update_status()
        if self.data['state'] in TASK_PENDING_STATES:
            return True

        return False

    def update_status(self):
        """
        Retrieve a task by its uri.

        Returns:
            task dict
        """
        task = self._connection.get("{}/{}".format(URL, self.data["id"]))
        self.data = task["task"]
        self.state = self.data["state"]

        return self.data

    def get_affected_resources(self):
        """
        Retrieve a resource associated with a task.

        Args:
            task: task dict

        Returns:
            list: list of resource ids
        """
        if self.state not in TASK_COMPLETED_STATES:
            raise exceptions.HPESimpliVityException(self.data["message"])

        affected_resources = self.data['affected_objects']

        return affected_resources
