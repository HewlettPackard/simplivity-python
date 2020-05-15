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
hosts = ovc.hosts

print("\n\nget_all with default params")
all_hosts = hosts.get_all()
count = len(all_hosts)
for host in all_hosts:
    print(f"{host}")
    print(f"{pp.pformat(host.data)} \n")

print("\n\nTotal number of hosts {}".format(count))
host_object = all_hosts[0]

print("\n\nget_all with filters")
all_hosts = hosts.get_all(filters={'name': host_object.data["name"]})
count = len(all_hosts)
for host in all_hosts:
    print(f"{host}")
    print(f"{pp.pformat(host.data)} \n")

print("\n\nTotal number of hosts {}".format(count))

print("\n\nget_all with pagination")
pagination = hosts.get_all(limit=105, pagination=True, page_size=50)
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
host = hosts.get_by_id(host_object.data["id"])
print(f"{host}")
print(f"{pp.pformat(host.data)} \n")

print("\n\nget_by_name")
host = hosts.get_by_name(host_object.data["name"])
print(f"{host}")
print(f"{pp.pformat(host.data)} \n")

print("\n\nget hardware details for the host")
host_hardware = host.get_hardware()
print(f"{pp.pformat(host_hardware)} \n")

print("\n\nget virtual controller shutdown status")
virtual_controller_status = host.get_virtual_controller_shutdown_status()
print("\n\nvirtual controller shutdown status : {}".format(virtual_controller_status))

print("\n\nshutdown virtual controller")
host = hosts.get_by_id(host_object.data["id"])
response = host.shutdown_virtual_controller()
print("\n\nshutdown virtual controller status : {}".format(response))
print("\n\nplease power on the virtual controller manually")
