###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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

from simplivity.ovc_client import OVC
from simplivity.exceptions import HPESimpliVityException

pp = pprint.PrettyPrinter(indent=4)

config = {
    "ip": "<ovc_ip>",
    "credentials": {
        "username": "<username>",
        "password": "<password>"
    }
}

ovc = OVC(config)
cluster_groups = ovc.cluster_groups

print("\n\nget_all with default params")
all_cluster_groups = cluster_groups.get_all()
for cluster_group in all_cluster_groups:
    print(f"{cluster_group}")
    print(f"{pp.pformat(cluster_group.data)} \n")
count = len(all_cluster_groups)
print(f"Total number of cluster groups : {count}")

cluster_group_object = all_cluster_groups[0]

cluster_group_name = cluster_group_object.data["name"]
print("\n\nget_all with name filter")
all_cluster_groups = cluster_groups.get_all(filters={'name': cluster_group_name})
for cluster_group in all_cluster_groups:
    print(f"{cluster_group}")
    print(f"{pp.pformat(cluster_group.data)} \n")
count = len(all_cluster_groups)
print(f"Total number of cluster groups : {count}")

print("\n\nget_all with pagination")
pagination = cluster_groups.get_all(limit=10, pagination=True, page_size=2)
end = False
while not end:
    data = pagination.data
    print(f"page size : {len(data['resources'])}")
    print(f"{pp.pformat(data)} \n")

    try:
        pagination.next_page()
    except HPESimpliVityException:
        end = True

cluster_group_id = cluster_group_object.data["id"]
print("\n\nget_by_id")
cluster_group = cluster_groups.get_by_id(cluster_group_id)
print(f"{cluster_group}")
print(f"{pp.pformat(cluster_group.data)} \n")

cluster_group_name = cluster_group_object.data["name"]
print("\n\nget_by_name")
cluster_group = cluster_groups.get_by_name(cluster_group_name)
print(f"{cluster_group}")
print(f"{pp.pformat(cluster_group.data)} \n")
