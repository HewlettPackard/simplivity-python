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

# variable declaration
management_ip = '<storeonce_management_ip>'
management_port = '<storeonce_management_port>'
external_store_type = '<external_store_type>'
external_store_name = '<storeonce_storename>'
username = '<storeonce_username>'
password = '<storeonce_password>'
storage_port = '<storage_port>'
cluster_name = '<cluster_name>'

pp = pprint.PrettyPrinter(indent=4)
ovc = OVC(config)
external_stores = ovc.external_stores
clusters = ovc.omnistack_clusters

print("\n\nget_all with default params")
all_external_stores = external_stores.get_all()
count = len(all_external_stores)
for external_store in all_external_stores:
    print(f"{external_store}")
    print(f"{pp.pformat(external_store.data)} \n")

print("\n\nTotal number of external stores {}".format(count))
external_store_object = all_external_stores[0]

print("\n\nget_all with filters")
all_external_stores = external_stores.get_all(filters={'name': external_store_object.data["name"]})
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

print("\n\nregister external store")
cluster_obj = clusters.get_by_name(cluster_name)
external_store_obj = external_stores.register_external_store(management_ip, external_store_name,
                                                             cluster_obj, username, password)

print(f"{external_store_obj}")
print(f"{pp.pformat(external_store_obj.data)} \n")

print("\n\nupdate external store access credential")
# We can provide the updated credential to access the external store
external_stores.update_credentials(external_store_name, username, password)

print("\n\nunregister external store")
cluster_obj = clusters.get_by_name(cluster_name)
external_store_obj.unregister_external_store(cluster_obj)
