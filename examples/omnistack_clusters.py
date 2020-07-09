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

from simplivity.ovc_client import OVC
from simplivity.exceptions import HPESimpliVityException

config = {
    "ip": "<ovc_ip>",
    "credentials": {
        "username": "<username>",
        "password": "<password>"
    }
}

pp = pprint.PrettyPrinter(indent=4)

ovc = OVC(config)
clusters = ovc.omnistack_clusters

# variable declaration
cluster_1_name = "cluster1"

print("\n\nget_all with default params")
all_clusters = clusters.get_all()
count = len(all_clusters)
for cluster in all_clusters:
    print(f"{cluster}")
    print(f"{pp.pformat(cluster.data)} \n")

print("\n\nTotal number of clusters {}".format(count))
cluster_object = all_clusters[0]

print("\n\nget_all with filters")
all_clusters = clusters.get_all(filters={'name': cluster_object.data["name"]})
count = len(all_clusters)
for cluster in all_clusters:
    print(f"{cluster}")
    print(f"{pp.pformat(cluster.data)} \n")

print("\n\nTotal number of clusters {}".format(count))

print("\n\nget_all with pagination")
pagination = clusters.get_all(limit=105, pagination=True, page_size=50)
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

print("\n\nget_by_id")
cluster = clusters.get_by_id(cluster_object.data["id"])
print(f"{cluster}")
print(f"{pp.pformat(cluster.data)} \n")

print("\n\nget_by_name")
cluster = clusters.get_by_name(cluster_object.data["name"])
print(f"{cluster}")
print(f"{pp.pformat(cluster.data)} \n")

print("\n\nget_time_zone_list")
time_zones = clusters.get_time_zone_list()
print(f"{pp.pformat(time_zones)} \n")

print("\n\nget_connected_clusters")
cluster1 = clusters.get_by_name(cluster_1_name)
connected_clusters = cluster1.get_connected_clusters()
print(f"{pp.pformat(connected_clusters)} \n")
cluster = clusters.get_all(show_optional_fields=True,
                           filters={'id': cluster.data["id"]})[0]
ori_time_zone = cluster.data['time_zone']

print("\n\nset_time_zone")
cluster = cluster.set_time_zone("Zulu")
print(f"{pp.pformat(cluster.data)} \n")
# revert to original time zone
cluster = cluster.set_time_zone(ori_time_zone)
print(f"{pp.pformat(cluster.data)} \n")

print("\n\nget_throughput")
cluster1 = clusters.get_by_name(cluster_1_name)
cluster_throuput = cluster1.get_throughput('', 0, 50)
print(f"{pp.pformat(cluster_throuput)} \n")

print("\n\nget metrics report for cluster")
cluster_metrics = cluster1.get_metrics()
print(f"{pp.pformat(cluster_metrics)} \n")
