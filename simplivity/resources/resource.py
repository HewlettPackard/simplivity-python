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

"""Implements helper methods for the resource classes."""

import logging
from urllib.parse import quote

from simplivity.resources.tasks import Task
from simplivity import exceptions

PAGE_SIZE_NOT_SET = "page_size param should be set when pagination is on"
PAGINATION_NO_MORE_PAGES = "No more pages"

logger = logging.getLogger(__name__)


def build_uri_with_query_string(base_url, kwargs):
    """Creates URL using base url and the parameters.

    Args:
        base_url: URL string.
        kwargs: Dictionary of parameters

    Returns:
        string: URL with query parameters
    """
    query_string = '&'.join('{}={}'.format(key, kwargs[key]) for key in sorted(kwargs))
    symbol = '?' if '?' not in base_url else '&'
    return "{}{}{}".format(base_url, symbol, query_string)


class Pagination(object):
    """Implements pagination features for get_all method."""

    def __init__(self, con, url, resource_obj, params, members_field, page_size):
        """Initializes Pagination class."""
        self._url = url
        self._resource_obj = resource_obj
        self._params = params
        self._members_field = members_field
        self._page_size = page_size
        self._connection = con

        self._total_count = params["limit"]
        self._params["limit"] = page_size
        self._params["offset"] = 0

        self._first_page = 1
        self._last_page = 1
        self._last_page_size = page_size

        if self._total_count > page_size:
            last_page, one_more_page = divmod(self._total_count, page_size)
            self._last_page = last_page
            if one_more_page:
                self._last_page += 1
                self._last_page_size = one_more_page

        self.data = {"resources": [], "page": 1,
                     "size": 0, "requested_pages": self._last_page}
        self._set_data()

    def next_page(self):
        """Gets next page.

        Returns list of resources from next page.

        Raises:
            HPESimpliVityException: if no more pages to return.
        """
        if self.data["page"] + 1 > self._last_page:
            raise exceptions.HPESimpliVityException(PAGINATION_NO_MORE_PAGES)

        self.data["page"] += 1

        if self.data["page"] == self._last_page:
            self._params["limit"] = self._last_page_size

        self._params["offset"] += self._page_size
        self._set_data()

        return self.data

    def previous_page(self):
        """Gets previous page.

        Returns list of resources from previous page.

        Raises:
            HPESimpliVityException: if no more pages to return.
        """
        if self.data["page"] - 1 < self._first_page:
            raise exceptions.HPESimpliVityException(PAGINATION_NO_MORE_PAGES)

        self.data["page"] -= 1

        self._params["limit"] = self._page_size
        self._params["offset"] -= self._page_size
        self._set_data()

        return self.data

    def _set_data(self):
        """
        Sets data(page size and the resources) of the current page.
        """
        url = build_uri_with_query_string(self._url, self._params)

        response = self._connection.get(url)
        resources = response.get(self._members_field, [])

        if not len(resources):
            raise exceptions.HPESimpliVityException(PAGINATION_NO_MORE_PAGES)

        for index, resource in enumerate(resources):
            resources[index] = self._resource_obj.get_by_data(resource)

        self.data["resources"] = resources
        self.data["size"] = len(resources)


class ResourceClient(object):
    """Implements helper methods for resource classes."""

    def __init__(self, connection, resource_obj):
        """Initializes with a resource object and connection."""
        self._resource_obj = resource_obj
        self._connection = connection

    def get_all(self, resource_url, members_field=None, pagination=False,
                page_size=0, limit=500, offset=0, sort=None, order='descending',
                filters=None, fields=None, case_sensitive=True,
                show_optional_fields=False):
        """Gets all resources.

        Args:
            resource_url: URL of the resource
            members_field: Name of the resource field(to fetch the resources from get call response)
            pagination: Default value is False, set to True if pagination is required
            page_size: Number of resources per page - mandatory field if pagination is on
            limit: A positive integer that represents the maximum number of results to return
            sort: The name of the field where the sort occurs
            order: The sort order preference, valid values: ascending or descending
            filters: Dictionary of filers, example: {'name': 'name'}
            fields: A comma-separated list of fields to include in the returned objects. Default: all
            case_sensitive: An indicator that specifies if the filter and sort results
              use a case-sensitive or insensitive manner. Default: True
            show_optional_fields: An indicator to show or not show the ha_status,
              ha_resynchronization_progress, hypervisor_virtual_machine_power_state, and hypervisor_is_template

        Returns:
             list/pagination object: Pagination object if pagination is on or list of resources
        """
        query_params = {"limit": limit,
                        "offset": offset,
                        "order": order}

        if filters and isinstance(filters, dict):
            query_params.update(filters)

        if fields:
            query_params["fields"] = quote(fields)

        if show_optional_fields:
            query_params["show_optional_fields"] = quote(show_optional_fields)

        query_params["sort"] = sort if sort else 'name'
        query_params["case"] = "sensitive" if case_sensitive else "insensitive"

        if pagination:
            if not page_size:
                raise exceptions.HPESimpliVityException(PAGE_SIZE_NOT_SET)

            out = Pagination(self._connection, resource_url, self._resource_obj,
                             query_params, members_field, page_size)
        else:
            url = build_uri_with_query_string(resource_url, query_params)
            response = self._connection.get(url)
            data_list = response.get(members_field, [])
            out = []
            for data in data_list:
                out.append(self._resource_obj.get_by_data(data))

        return out

    def task_affected_resources(self, task, timeout):
        """Handles asynchronous calls.

        Args:
            task: Task data retunrned by a REST call
            timeout: Timeout value

        Returns:
            list: Returns ids of affected resources
        """
        task_obj = Task(self._connection, task)
        affected_resources = task_obj.wait_for_task(timeout)

        return affected_resources

    def do_get(self, uri):
        """Makes get requests

        Args:
            uri: URI of the resource

        Returns:
            Returns: Returns the resource data
        """
        return self._connection.get(uri)

    def do_post(self, uri, data, timeout, custom_headers):
        """Makes post requests.

        Args:
            uri: URI of the resource.
            data: Request body of the call
            timeout: Time out for the request in seconds.
            cutom_headers: Allows to add custom http headers.

        Returns:
            list: Returns ids of the affected resources.
        """
        task, entity = self._connection.post(uri, data, custom_headers=custom_headers)

        if not task:
            return entity

        return self.task_affected_resources(task, timeout)

    def do_put(self, uri, data, timeout, custom_headers):
        """Makes put requests.

        Args:
            uri: URI of the resource
            data: Request body of the call
            timeout: Time out for the request in seconds.
            custom_headers: Allows to set custom http headers.

        Retuns:
            list: Returns ids of the  affected resources.
        """
        task, body = self._connection.put(uri, data, custom_headers=custom_headers)

        if not task:
            return body

        return self.task_affected_resources(task, timeout)


class ResourceBase(object):
    """Implements base class for resource classes."""

    def __init__(self, connection):
        """Initializes class with connection and resource client."""
        self._connection = connection
        self._client = ResourceClient(self._connection, self)

    def get_by_name(self, name):
        """Gets resource by name.

        Args:
            name: Name of the resource

        Returns:
            object: object of the resource

        Raises:
            HPESimpliVityResourceNotFound: if resource doesn't exist with the name passed.
        """
        resources = self.get_all(filters={'name': name})
        if not len(resources):
            raise exceptions.HPESimpliVityResourceNotFound("Resource not found with the name {}".format(name))

        return resources[0]

    def get_by_id(self, resource_id):
        """Gets resource by id.

        Args:
            id: ID of the resource

        Returns:
            object: Resource object

        Raises:
            HPESimpliVityResourceNotFound: if resource doesn't exist with the id passed.
        """
        resources = self.get_all(filters={'id': resource_id})
        if not len(resources):
            raise exceptions.HPESimpliVityResourceNotFound("Resource not found with the id {}".format(resource_id))

        return resources[0]
