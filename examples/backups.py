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
import time
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
backups = ovc.backups
machines = ovc.virtual_machines
datastores = ovc.datastores

# variable declaration
test_vm_name = "test_MySql-VM_restore"
remote_datastore = "remoteDS"
cluster1_name = "CC_Virt_0001"
cluster2_name = "CC_Virt_0000"

print("\n\nget_all with default params")
all_backups = backups.get_all()
count = len(all_backups)
for backup in all_backups:
    print(f"{backup}")
    print(f"{pp.pformat(backup.data)} \n")

print("\n\nTotal number of backups {}".format(count))
backup_object = all_backups[0]

print("\n\nget_all with filters")
all_backups = backups.get_all(filters={'name': backup_object.data["name"]})
for backup in all_backups:
    print(f"{backup}")
    print(f"{pp.pformat(backup.data)} \n")


print("\n\nget_all with pagination")
pagination = backups.get_all(limit=105, pagination=True, page_size=50)

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
backup = backups.get_by_id(backup_object.data["id"])
print(f"{backup}")
print(f"{pp.pformat(backup.data)} \n")

print("\n\nget_by_name")
backup = backups.get_by_name(backup_object.data["name"])
print(f"{backup}")
print(f"{pp.pformat(backup.data)} \n")

print("Create backup for the testing the restore functionality")
vm = machines.get_by_name(test_vm_name)
backup = vm.create_backup("backup_test_from_sdk_" + str(time.time()), retention=120)
print(f"{backup}")
print(f"{pp.pformat(backup.data)} \n")

# Create the new virtual machine on the same datastore
restored_vm = backup.restore(False, "Restored_Machine_SDK_Same_DS")
print(f"{restored_vm}")
print(f"{pp.pformat(restored_vm.data)} \n")

# Resets the original virtual machine to the same state it was in when the backup was created
restored_vm = backup.restore(True)
print(f"{restored_vm}")
print(f"{pp.pformat(restored_vm.data)} \n")

print("\nget the remote datastore for the restoring the VM ")
datastore_object = datastores.get_by_name(remote_datastore)

print(f"{datastore_object}")
print(f"{pp.pformat(datastore_object.data)} \n")

# Create the new virtual machine on the different datastore by passing object
restored_vm = backup.restore(False, "Restored_Machine_SDK_anotherDS_Object", datastore_object)
print(f"{restored_vm}")
print(f"{pp.pformat(restored_vm.data)} \n")

# Create the new virtual machine on the different datastore by passing name
restored_vm = backup.restore(False, "Restored_Machine_SDK_anotherDS_Name", datastore_object.data["name"])
print(f"{restored_vm}")
print(f"{pp.pformat(restored_vm.data)} \n")

print("\n\nsaves the specified backup to prevent it from expiring, verify: expiration_time set to NA")
backup.lock()
print(f"{backup}")
print(f"{pp.pformat(backup.data)} \n")

print("\n\nrename the backup")
backup.rename(f"renamed_{backup.data['name']}")
print(f"{backup}")
print(f"{pp.pformat(backup.data)} \n")

backup.delete()

print("\n\ncopy backup")
backup = vm.create_backup("backup_test_from_sdk_" + str(time.time()), cluster1_name)
print(f"{backup}")
print(f"{pp.pformat(backup.data)} \n")

copy_backup = backup.copy(cluster2_name)
print(f"{copy_backup}")
print(f"{pp.pformat(copy_backup.data)} \n")

copy_backup.delete()
backup.delete()

print("\n\nset retention")
vm = machines.get_by_name(test_vm_name)
backup1 = vm.create_backup("backup_test_from_sdk_set_retention1_" + str(time.time()))
print(f"{backup1}")
print(f"{pp.pformat(backup1.data)} \n")
backup2 = vm.create_backup("backup_test_from_sdk_set_retention2_" + str(time.time()))
print(f"{backup2}")
print(f"{pp.pformat(backup2.data)} \n")

backup_list = [backup1, backup2]
backup_obj = backups.set_retention(backup_list, 10)

for backup in backup_obj:
    print(f"{backup}")
    print(f"{pp.pformat(backup.data)} \n")

backups.delete_multiple_backups(backup_list)
