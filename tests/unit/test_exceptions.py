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

import unittest
import os
import tempfile
import pickle

from simplivity import exceptions


class ExceptionsTest(unittest.TestCase):
    def test_exception_constructor_with_string(self):
        exception = exceptions.HPESimpliVityException("A message string")

        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)

    def test_exception_constructor_with_valid_dict(self):
        exception = exceptions.HPESimpliVityException({'message': "A message string"})

        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.response, {'message': "A message string"})
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(exception.args[1], {'message': 'A message string'})

    def test_exception_constructor_with_invalid_dict(self):
        exception = exceptions.HPESimpliVityException({'msg': "A message string"})

        self.assertEqual(exception.msg, None)
        self.assertEqual(exception.response, {'msg': "A message string"})
        self.assertEqual(exception.args[0], None)
        self.assertEqual(exception.args[1], {'msg': "A message string"})

    def test_exception_constructor_with_invalid_type(self):
        exception = exceptions.HPESimpliVityException(['List, item 1', "List, item 2: A message string"])

        self.assertEqual(exception.msg, None)
        self.assertEqual(exception.response, ['List, item 1', "List, item 2: A message string"])
        self.assertEqual(exception.args[0], None)
        self.assertEqual(exception.args[1], ['List, item 1', "List, item 2: A message string"])

    def test_exception_constructor_with_unicode(self):
        exception = exceptions.HPESimpliVityException(u"A message string")

        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)

    def test_task_error_constructor_with_string(self):
        exception = exceptions.HPESimpliVityTaskError("A message string", 100)

        self.assertIsInstance(exception, exceptions.HPESimpliVityException)
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)
        self.assertEqual(exception.error_code, 100)

    def test_simplivity_resource_not_found_inheritance(self):
        exception = exceptions.HPESimpliVityResourceNotFound("The resource was not found!")

        self.assertIsInstance(exception, exceptions.HPESimpliVityException)
        self.assertEqual(exception.msg, "The resource was not found!")
        self.assertEqual(exception.response, None)
        self.assertEqual(exception.args[0], "The resource was not found!")

    def test_pickle_HPESimpliVityException_dict(self):
        message = {"msg": "test message"}
        exception = exceptions.HPESimpliVityException(message)
        tempf = tempfile.NamedTemporaryFile(delete=False)
        with tempf as f:
            pickle.dump(exception, f)

        with open(tempf.name, 'rb') as f:
            exception = pickle.load(f)

        os.remove(tempf.name)
        self.assertEqual('HPESimpliVityException', exception.__class__.__name__)

    def test_pickle_HPESimpliVityException_message(self):
        message = "test message"
        exception = exceptions.HPESimpliVityException(message)
        tempf = tempfile.NamedTemporaryFile(delete=False)
        with tempf as f:
            pickle.dump(exception, f)

        with open(tempf.name, 'rb') as f:
            exception = pickle.load(f)

        os.remove(tempf.name)
        self.assertEqual('HPESimpliVityException', exception.__class__.__name__)


if __name__ == '__main__':
    unittest.main()
