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
policies = ovc.policies

print("\n\n get_all with default params")
all_policies = policies.get_all()
count = len(all_policies)
for policy in all_policies:
    print(policy)

print("\nTotal number of policies {}".format(count))
policy_object = all_policies[0]

print("\n\n get_all with filers")
all_policies = policies.get_all(filters={'name': policy_object.data["name"]})
count = len(all_policies)
for policy in all_policies:
    print(policy)

print("\n Total number of policies {}".format(count))

print("\n\n get_all with pagination")
pagination = policies.get_all(limit=105, pagination=True, page_size=50)
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
policy = policies.get_by_id(policy_object.data["id"])
print(policy, policy.data)

print("\n\n get_by_name")
policy = policies.get_by_name(policy_object.data["name"])
print(policy, policy.data)

print("\n\n get_all VMs using this policy")
vms = policy.get_vms()
print(policy.data)
print(vms)
