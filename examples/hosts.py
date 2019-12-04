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

from simplivity.ovc_client import OVC
from simplivity.exceptions import HPESimpliVityException

config = {
    "ip": "<ovc_ip>",
    "credentials": {
        "username": "<username>",
        "password": "<password>"
    }
}

ovc = OVC(config)
hosts = ovc.hosts

print("\n\n get_all with default params")
all_hosts = hosts.get_all()
count = len(all_hosts)
for host in all_hosts:
    print(host.data)

print("\nTotal number of hosts {}".format(count))
host_object = all_hosts[0]

print("\n\n get_all with filers")
all_hosts = hosts.get_all(filters={'name': host_object.data["name"]})
count = len(all_hosts)
for host in all_hosts:
    print(host.data)

print("\n Total number of hosts {}".format(count))

print("\n\n get_all with pagination")
pagination = hosts.get_all(limit=105, pagination=True, page_size=50)
end = False
while not end:
    data = pagination.data
    print("Page size:", len(data["resources"]))
    print(data)

    try:
        pagination.next_page()
    except HPESimpliVityException:
        end = True

print("\n\n get_by_id")
hosst = hosts.get_by_id(host_object.data["id"])
print(host, host.data)

print("\n\n get_by_name")
host = hosts.get_by_name(host_object.data["name"])
print(host, host.data)
