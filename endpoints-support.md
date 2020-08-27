Refer SimpliVity REST API doc for the resource endpoints documentation [HPE SimpliVity REST API Documentation](https://developer.hpe.com/api/simplivity/).

<br />

## Supported resources and endpoints

| Endpoints                                                                                  | Action |
| ------------------------------------------------------------------------------------------ | ------ |
|     **Backups**
|<sub>/backups</sub>                                                                         |GET     |
|<sub>/backups/delete</sub>                                                                  |POST    |
|<sub>/backups/set_retention</sub>                                                           |POST    |
|<sub>/backups/{bkpId}</sub>                                                                 |DELETE  |
|<sub>/backups/{bkpId}/cancel</sub>                                                          |POST    |
|<sub>/backups/{bkpId}/copy</sub>                                                            |POST    |
|<sub>/backups/{bkpId}/lock</sub>                                                            |POST    |
|<sub>/backups/{bkpId}/rename</sub>                                                          |POST    |
|<sub>/backups/{bkpId}/restore</sub>                                                         |POST    |
|<sub>/backups/{bkpId}/virtual_disk_partitions</sub>                                         |GET     |
|<sub>/backups/{bkpId}/virtual_disk_partition_files</sub>                                    |GET     |
|     **Cluster Groups**
|<sub>/cluster_groups</sub>                                                                  |GET     |
|<sub>/cluster_groups/{clusterGroupId}/rename</sub>                                          |POST    |
|     **Datastores**
|<sub>/datastores</sub>                                                                      |GET     |
|<sub>/datastores</sub>                                                                      |POST    |
|<sub>/datastores/{datastoreId}</sub>                                                        |DELETE  |
|<sub>/datastores/{datastoreId}/resize</sub>                                                 |POST    |
|<sub>/datastores/{datastoreId}/set_policy</sub>                                             |POST    |
|<sub>/datastores/{datastoreId}/share</sub>                                                  |POST    |
|<sub>/datastores/{datastoreId}/standard_hosts</sub>                                         |GET     |
|<sub>/datastores/{datastoreId}/unshare</sub>                                                |POST    |
|     **External Stores**
|<sub>/external_stores</sub>                                                                 |GET     |
|<sub>/external_stores</sub>                                                                 |POST    |
|<sub>/external_stores/unregister</sub>                                                      |POST    |
|<sub>/external_stores/update_credentials</sub>                                              |POST    |
|     **Hosts**
|<sub>/hosts</sub>                                                                           |GET     |
|<sub>/hosts/{hostId}/cancel_virtual_controller_shutdown</sub>                               |POST    |
|<sub>/hosts/{hostId}/capacity</sub>                                                         |GET     |
|<sub>/hosts/{hostId}/metrics</sub>                                                          |GET     |
|<sub>/hosts/{hostId}/remove_from_federation</sub>                                           |POST    |
|<sub>/hosts/{hostId}/hardware</sub>                                                         |GET     |
|<sub>/hosts/{hostId}/shutdown_virtual_controller</sub>                                      |POST    |
|<sub>/hosts/{hostId}/virtual_controller_shutdown_status</sub>                               |GET     |
|     **OmniStack Clusters**
|<sub>/omnistack_clusters</sub>                                                              |GET     |
|<sub>/omnistack_clusters/time_zone_list</sub>                                               |GET     |
|<sub>/omnistack_clusters/{clusterId}/connected_clusters</sub>                               |GET     |
|<sub>/omnistack_clusters/{clusterId}/metrics</sub>                                          |GET     |
|<sub>/omnistack_clusters/{clusterId}/set_time_zone</sub>                                    |POST    |
|<sub>/omnistack_clusters/{clusterId}/throughput</sub>                                       |GET     |
|     **Policies**
|<sub>/policies</sub>                                                                        |GET     |
|<sub>/policies</sub>                                                                        |POST    |
|<sub>/policies/policy_schedule_report</sub>                                                 |GET     |
|<sub>/policies/resume </sub>                                                                |POST    |
|<sub>/policies/suspend</sub>                                                                |POST    |
|<sub>/policies/{policyId}</sub>                                                             |DELETE  |
|<sub>/policies/{policyId}/impact_report/create_rules</sub>                                  |POST    |
|<sub>/policies/{policyId}/impact_report/edit_rules</sub>                                    |POST    |
|<sub>/policies/{policyId}/rename</sub>                                                      |POST    |
|<sub>/policies/{policyId}/rules</sub>                                                       |POST    |
|<sub>/policies/{policyId}/rules/{ruleId}</sub>                                              |GET     |
|<sub>/policies/{policyId}/rules/{ruleId}</sub>                                              |DELETE  |
|<sub>/policies/{policyId}/rules/{ruleId}</sub>                                              |PUT     |
|<sub>/policies/{policyId}/rules/{ruleId}/impact_report/delete_rule</sub>                    |POST    |
|     **Security**
|<sub>/security/certificates</sub>                                                           |GET     |
|<sub>/security/certificates</sub>                                                           |POST    |
|     **Virtual Machines**
|<sub>/virtual_machines</sub>                                                                |GET     |
|<sub>/virtual_machines/policy_impact_report/apply_policy</sub>                              |POST    |
|<sub>/virtual_machines/set_policy</sub>                                                     |POST    |
|<sub>/virtual_machines/{vmId}</sub>                                                         |GET     |
|<sub>/virtual_machines/{vmId}/backup</sub>                                                  |POST    |
|<sub>/virtual_machines/{vmId}/backup_parameters</sub>                                       |POST    |
|<sub>/virtual_machines/{vmId}/backups</sub>                                                 |GET     |
|<sub>/virtual_machines/{vmId}/clone</sub>                                                   |POST    |
|<sub>/virtual_machines/{vmId}/metrics</sub>                                                 |GET     |
|<sub>/virtual_machines/{vmId}/move</sub>                                                    |POST    |
|<sub>/virtual_machines/{vmId}/power_off</sub>                                               |POST    |
|<sub>/virtual_machines/{vmId}/power_on</sub>                                                |POST    |
|<sub>/virtual_machines/{vmId}/set_policy</sub>                                              |POST    |
|<sub>/virtual_machines/{vmId}/validate_backup_credentials</sub>                             |POST    |
