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

pp = pprint.PrettyPrinter(indent=4)

config = {
    "ip": "<ovc_ip>",
    "credentials": {
        "username": "<username>",
        "password": "<password>"
    }
}

ovc = OVC(config)
policies = ovc.policies
hosts = ovc.hosts
clusters = ovc.omnistack_clusters
cluster_groups = ovc.cluster_groups

print("\n\nget_all with default params")
all_policies = policies.get_all()
count = len(all_policies)
for policy in all_policies:
    print(f"{policy}")
    print(f"{pp.pformat(policy.data)} \n")

print(f"Total number of policies : {count}")
policy_object = all_policies[0]

print("\n\nget_all with filters")
all_policies = policies.get_all(filters={'name': policy_object.data["name"]})
count = len(all_policies)
for policy in all_policies:
    print(f"{policy}")
    print(f"{pp.pformat(policy.data)} \n")

print(f"Total number of policies : {count}")

print("\n\nget_all with pagination")
pagination = policies.get_all(limit=105, pagination=True, page_size=50)
end = False
while not end:
    data = pagination.data
    print("Page size:", len(data["resources"]))
    print(f"{pp.pformat(data)}")

    try:
        pagination.next_page()
    except HPESimpliVityException:
        end = True

print("\n\nget_by_id")
policy = policies.get_by_id(policy_object.data["id"])
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")

print("\n\nget_by_name")
policy = policies.get_by_name(policy_object.data["name"])
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")

print("\n\nget_all VMs using this policy")
vms = policy.get_vms()
print(policy.data)
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")
print(f"{pp.pformat(vms)} \n")

print("\n\ncreate policy")
policy_name = "fixed_frequency_retention_policy"
policy = policies.create(policy_name)
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")
multiple_rules = [
    {
        "start_time": "14:30",
        "end_time": "15:30",
        "application_consistent": False,
        "frequency": 3,
        "retention": 5
    },
    {
        "frequency": 5,
        "retention": 6
    }
]

print("\n\nadd rules to policy")
policy.create_rules(multiple_rules)
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")
single_rule = {
    "frequency": 10,
    "retention": 12
}
policy.create_rules(single_rule)
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")

print("\n\nget rule")
all_rules = policy.data["rules"]
for rule in all_rules:
    rule_obj = policy.get_rule(rule.get('id'))
    print(f"{pp.pformat(rule_obj)} \n")

print("\n\ndelete rule")
rule_id = policy.data["rules"][0]['id']
policy.delete_rule(rule_id)
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")

print("\n\nsuspend policy on host")
host = hosts.get_all()[0]
policies.suspend(host)

print("\n\nsuspend policy on omnistack_cluster")
cluster = clusters.get_all()[0]
policies.suspend(cluster)

""" cluster_group options works only with setup having MVA, please use below code for setup with MVA
cluster_group = cluster_groups.get_all()[0]
print(f"{cluster_group}")
print(f"{pp.pformat(cluster_group.data)} \n")
policies.suspend(cluster_group)
"""
""" federation options works only with setup NOT having MVA, please use below code for setup without MVA
print("\n\nsuspend policy on federation")
policies.suspend()
"""

print("\n\nrename policy")
policy.rename(f"renamed_{policy.data['name']}")
print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")

print("\n\ndelete policy")
policy.delete()
