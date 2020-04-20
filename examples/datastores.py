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
import time

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

ovc = OVC(config)
datastores = ovc.datastores

print("\n\nget_all with default params")
all_datastores = datastores.get_all()
for datastore in all_datastores:
    print(f"{datastore}")
    print(f"{pp.pformat(datastore.data)} \n")
count = len(all_datastores)
print(f"Total number of datastores : {count}")

# obtain cluster object for datastore create
clusters = ovc.omnistack_clusters
all_clusters = clusters.get_all()
cluster_object = all_clusters[0]
# obtain policy object for datastore create
policies = ovc.policies
all_policies = policies.get_all()
policy_object = all_policies[0]
print("\n\ndatastore create")
datastore_object = datastores.create("datastore_test_from_sdk_" + str(time.time()), cluster_object, policy_object, 1024)
print(f"{datastore_object}")
print(f"{pp.pformat(datastore_object.data)} \n")

datastore_name = datastore_object.data["name"]
print("\n\nget_all with name filter")
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

# Resize the datastore add 1 GB to existing size
print("\n\nresize the datastore")
datastore_size = datastore_object.data["size"] + 1073741824
datastore_object = datastore_object.resize(datastore_size)
print(f"{datastore_object}")
print(f"{pp.pformat(datastore_object.data)} \n")

# Set policy to the datastore
print("\n\nset policy on the datastore")
policy_object = policies.create("fixed_retention_policy")
print(f"{policy_object}")
print(f"{pp.pformat(policy_object.data)} \n")

datastore_object.set_policy(policy_object)
print(f"{datastore_object}")
print(f"{pp.pformat(datastore_object.data)} \n")

print("\n\ndatastore delete")
all_datastores = datastores.get_all()
count = len(all_datastores)
print(f"Total number of datastores before delete: {count} \n")
datastore_object.delete()

# delete the new policy created
policy_object.delete()
print(f"{datastore_object}")
print(f"{pp.pformat(datastore_object.data)} \n")

all_datastores = datastores.get_all()
count = len(all_datastores)
print(f"Total number of datastores after delete: {count}")
