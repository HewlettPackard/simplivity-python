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

import time

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

# Create resource clients
ovc = OVC(config)
machines = ovc.virtual_machines
policies = ovc.policies
datastores = ovc.datastores
omnistack_clusters = ovc.omnistack_clusters

# variable declaration
vm_1_name = "health_tool_move_test"
vm_2_name = "new_vm_for_sdk_test"
datastore_1_name = "SVT-DS1"
datastore_2_name = "DS2"
policy_name = "Simple"
omnistack_cluster_name = "Epyc"

print("\n\n get_all with default params")
vms = machines.get_all()
count = len(vms)
for vm in vms:
    print(f"{pp.pformat(vm.data)} \n")

print(f"Total number of vms : {count}")

vm_object = vms[0]

print("\n\n get_all with filers")
vms = machines.get_all(filters={'name': vm_object.data["name"]})
count = len(vms)
for vm in vms:
    print(f"{pp.pformat(vm.data)} \n")
print(f"Total number of vms : {count}")

print("\n\n get_all with pagination")
pagination = machines.get_all(limit=500, pagination=True, page_size=50)
end = False
while not end:
    data = pagination.data
    print("Page size:", len(data["resources"]))
    print(f"{pp.pformat(data)}")
    try:
        pagination.next_page()
    except HPESimpliVityException:
        end = True

print("\n\n get_by_id")
vm = machines.get_by_id(vm_object.data["id"])
print(f"{vm}")
print(f"{pp.pformat(vm.data)} \n")

print("\n\n get_by_name")
vm1 = machines.get_by_name(vm_1_name)
print(f"{vm1}")
print(f"{pp.pformat(vm1.data)} \n")

vm2 = machines.get_by_name(vm_2_name)
print(f"{vm2}")
print(f"{pp.pformat(vm2.data)} \n")

policy = policies.get_by_name(policy_name)

print(f"{policy}")
print(f"{pp.pformat(policy.data)} \n")

print("\n\n get_backups")
backups = vm2.get_backups()
for backup in backups:
    print(f"{pp.pformat(backup.data)} \n")

print("\n\n set_policy_for_multiple_vms")
vms = [vm1, vm2]
response = machines.set_policy_for_multiple_vms(policy, vms)
for vm in response:
    print(f"{vm}")
    print(f"{pp.pformat(vm.data)} \n")

print("\n\n clone")
cloned_vm = vm1.clone(vm_1_name + " clone_test")
print(f"{cloned_vm}")
print(f"{pp.pformat(cloned_vm.data)} \n")


print("\n\n clone and move to different datastore")
print("VM id :", vm1.data["id"])
cloned_vm = vm1.clone(vm_1_name + " clone_move_test", datastore=datastore_2_name)

print("\nMoved vm details")
print(f"{cloned_vm}")
print(f"{pp.pformat(cloned_vm.data)} \n")

print("\nMove VM to different datastore using datastore's name")
print("\n VM data before move")
print(f"{pp.pformat(vm1.data)} \n")

newvm = vm2.move(vm_2_name + "_move_test", datastore_2_name)
print("\n New VM details, after move")
print(f"{pp.pformat(newvm.data)} \n")

newvm = newvm.move(vm_2_name, datastore_1_name)
print("\n Move VM back to the original datastore")
print(f"{pp.pformat(newvm.data)} \n")

print("\n Move using datastore object")
datastore = datastores.get_by_name(datastore_2_name)
newvm = vm2.move(vm_2_name + "move_with_obj", datastore)
print(f"{pp.pformat(newvm.data)} \n")

print("\n Move VM back to the original datastore")
newvm = newvm.move(vm_2_name, datastore_1_name)
print(f"{pp.pformat(newvm.data)} \n")

print("\n create_backup")
cluster = omnistack_clusters.get_by_name(omnistack_cluster_name)
print(f"{cluster}")
print(f"{pp.pformat(cluster.data)} \n")

vm_backup = vm2.create_backup("backup_test_from_sdk_" + str(time.time()), cluster)
print(f"{pp.pformat(vm_backup.data)} \n")

print("Get backups of a single vm")
backups = vm2.get_backups()
pp.pprint(backups)

print("\n Set backup parameters of a VM")
guest_username = "svt"
guest_password = "svtpassword"
set_parameters = vm1.set_backup_parameters(guest_username, guest_password)
print(f"{pp.pformat(set_parameters.data)} \n")

print("\n Set policy")
vm1 = machines.get_by_name(vm_1_name)
set_policy = vm1.set_policy(policy_name)
print(f"{pp.pformat(set_policy.data)} \n")

print("\n Power off")
vm1 = machines.get_by_name(vm_1_name)
vm_powered_off = vm1.power_off()
print(f"{pp.pformat(vm_powered_off.data)} \n")
