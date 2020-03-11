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

import pprint

from simplivity.exceptions import HPESimpliVityException
from simplivity.ovc_client import OVC

pp = pprint.PrettyPrinter(indent=4)

config = {
    "ip": "<ovc_ip>",
    "credentials": {
        "username": "<username>",
        "password": "<password>"
    }
}

config = {
    "ip": "10.1.218.241",
    "credentials": {
        "username": "administrator@vsphere.local",
        "password": "svtrfs29L@B",
    },
}

ovc = OVC(config)
datastores = ovc.datastores

print("\n\nget_all with default params")
all_datastores = datastores.get_all()
for datastore in all_datastores:
    print(f"{datastore}")
    print(f"{pp.pformat(datastore.data)} \n")
count = len(all_datastores)
print(f"Total number of datastores : {count}")

datastore_object = all_datastores[0]

datastore_name = datastore_object.data["name"]
print("\n\nget_all with filters")
all_datastores = datastores.get_all(filters={'name': datastore_name})
for datastore in all_datastores:
    print(f"{datastore}")
    print(f"{pp.pformat(datastore.data)} \n")
count = len(all_datastores)
print(f"Total number of datastores : {count}")

print("\n\nget_all with pagination")
pagination = datastores.get_all(limit=10, pagination=True, page_size=2)
end = False
while not end:
    data = pagination.data
    print(f"page size : {len(data['resources'])}")
    print(f"{pp.pformat(data)} \n")

    try:
        pagination.next_page()
    except HPESimpliVityException:
        end = True

datastore_id = datastore_object.data["id"]
print("\n\nget_by_id")
datastore = datastores.get_by_id(datastore_id)
print(f"{datastore}")
print(f"{pp.pformat(datastore.data)} \n")

datastore_name = datastore_object.data["name"]
print("\n\nget_by_name")
datastore = datastores.get_by_name(datastore_object.data["name"])
print(f"{datastore}")
print(f"{pp.pformat(datastore.data)} \n")
