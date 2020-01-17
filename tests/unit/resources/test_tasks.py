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
from mock import mock, call

from simplivity.connection import Connection
from simplivity.resources.tasks import Task
from simplivity import exceptions

ERR_MSG = "Message error"


class TaskTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = Connection(self.host)
        self.task_data = {"state": "IN_PROGRESS", 'id': '123456'}
        self.task = Task(self.connection, self.task_data)

    @mock.patch.object(Connection, 'get')
    def test_is_task_running(self, mock_get):
        mock_get.return_value = {'task': self.task_data}
        self.assertTrue(self.task.is_task_running())

    @mock.patch.object(Connection, 'get')
    def test_is_task_running_false(self, mock_get):
        updated_task_data = self.task_data.copy()
        updated_task_data["state"] = 'COMPLETED'
        mock_get.return_value = {'task': updated_task_data}

        self.assertFalse(self.task.is_task_running())

    @mock.patch.object(Connection, 'get')
    def test_is_task_running_with_generic_failure(self, mock_get):
        mock_get.side_effect = Exception(ERR_MSG)
        self.assertRaises(Exception, self.task.is_task_running)

    @mock.patch.object(Task, 'is_task_running')
    def test_wait_for_task_timeout(self, mock_is_running):
        mock_is_running.return_value = True
        timeout = 2

        with self.assertRaises(exceptions.HPESimpliVityTimeout) as error:
            self.task.wait_for_task(timeout)

        self.assertEqual('Waited {} seconds for task to complete, aborting'.format(timeout),
                         error.exception.msg)

    @mock.patch.object(Task, 'is_task_running')
    @mock.patch('time.sleep')
    def test_wait_for_task_increasing_sleep(self, mock_sleep, mock_is_running):

        mock_is_running.return_value = True
        timeout = 0.1

        # should call sleep increasing 1 until 10
        calls = [call(1), call(2), call(3), call(4), call(5), call(6), call(7),
                 call(8), call(9), call(10), call(10), call(10)]

        with self.assertRaises(exceptions.HPESimpliVityTimeout) as error:
            self.task.wait_for_task(timeout)

        mock_sleep.assert_has_calls(calls)
        self.assertEqual('Waited {} seconds for task to complete, aborting'.format(timeout),
                         error.exception.msg)

    @mock.patch.object(Task, 'is_task_running')
    @mock.patch.object(Connection, 'get')
    def test_wait_for_task(self, mock_get, mock_is_running):
        task = {'state': 'COMPLETED', 'id': '12345'}
        affected_objects = ['12345']
        self.task.data = task

        mock_is_running.return_value = False
        task_completed = task.copy()
        task_completed["affected_objects"] = affected_objects
        mock_get.return_value = {'task': task_completed}

        ret_entity = self.task.wait_for_task()
        self.assertEqual(ret_entity, affected_objects)


if __name__ == '__main__':
    unittest.main()
