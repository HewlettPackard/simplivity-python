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

from simplivity.ovc_client import OVC
from simplivity.exceptions import HPESimpliVityException
import pprint

config = {
    "ip": "<ovc_ip>",
    "credentials": {
        "username": "<username>",
        "password": "<password>"
    }
}

pp = pprint.PrettyPrinter(indent=4)
ovc = OVC(config)
external_stores = ovc.external_stores

print("\n\nget_all with default params")
all_external_stores = external_stores.get_all()
count = len(all_external_stores)
for external_store in all_external_stores:
    print(f"{external_store}")
    print(f"{pp.pformat(external_store.data)} \n")

print("\n\nTotal number of backups {}".format(count))
backup_object = all_external_stores[0]

print("\n\nget_all with filters")
all_external_stores = external_stores.get_all(filters={'name': backup_object.data["name"]})
for external_store in all_external_stores:
    print(f"{external_store}")
    print(f"{pp.pformat(external_store.data)} \n")

print("\n\nget_all with pagination")
pagination = external_stores.get_all(limit=105, pagination=True, page_size=50)

end = False
while not end:
    data = pagination.data
    count = len(data["resources"])
    print(f"Page size: {count}")
    print(f"{pp.pformat(data)}")

    try:
        pagination.next_page()
    except HPESimpliVityException:
        end = True
