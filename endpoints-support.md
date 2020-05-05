Refer SimpliVity REST API doc for the resource endpoints documentation [HPE SimpliVity REST API Documentation](https://developer.hpe.com/api/simplivity/).

<br />

## Supported resources and endpoints

| Endpoints                                                                               | Action   |
| --------------------------------------------------------------------------------------- | -------- |
|     **Backups**
|<sub>/backups	</sub>                                                                    |GET       |
|<sub>/backups/delete  </sub>                                                             |POST      |
|<sub>/backups/{bkpId}  </sub>                                                            |DELETE    |
|<sub>/backups/{bkpId}/restore  </sub>                                                    |POST      |
|     **Cluster Groups**
|<sub>/cluster_groups  </sub>                                                             |GET       |
|     **Datastores**
|<sub>/datastores	</sub>                                                                |GET       |
|<sub>/datastores	</sub>                                                                |POST       |
|<sub>/datastores/{datastoreId}  </sub>                                                   |DELETE    |
|<sub>/datastores/{datastoreId}/resize  </sub>                                            |POST      |
|<sub>/datastores/{datastoreId}/set_policy  </sub>                                        |POST      |
|     **Hosts**
|<sub>/hosts	</sub>                                                                    |GET       |
|<sub>/hosts/{hostId}/remove_from_federation  </sub>						|POST      |
|<sub>/hosts/{hostId}/hardware  </sub>						          |GET      |
|<sub>/hosts/{hostId}/virtual_controller_shutdown_status  </sub>                          |GET      |
|     **OmniStack Clusters**
|<sub>/omnistack_clusters	</sub>                                                        |GET       |
|     **Policies**
|<sub>/policies	</sub>                                                                    |GET       |
|<sub>/policies</sub>                                                                     |POST      |
|<sub>/policies/{policyId} </sub>                                                         |DELETE    |
|<sub>/policies/{policyId}/rules </sub>                                                   |POST      |
|<sub>/policies/{policyId}/rules/{ruleId} </sub>                                          |GET       |
|<sub>/policies/{policyId}/rules/{ruleId} </sub>                                          |DELETE    |
|     **Virtual Machines**
|<sub>/virtual_machines	</sub>                                                            |GET       |
|<sub>/virtual_machines/set_policy	</sub>                                                |POST      |
|<sub>/virtual_machines/{vmId}	</sub>                                                    |GET       |
|<sub>/virtual_machines/{vmId}/backup	</sub>                                            |POST      |
|<sub>/virtual_machines/{vmId}/backup_parameters	</sub>                                |POST      |
|<sub>/virtual_machines/{vmId}/backups	</sub>                                            |GET       |
|<sub>/virtual_machines/{vmId}/clone	</sub>                                            |POST      |
|<sub>/virtual_machines/{vmId}/move	</sub>                                                |POST      |
|<sub>/virtual_machines/{vmId}/power_off	</sub>                                        |POST      |
|<sub>/virtual_machines/{vmId}/set_policy	</sub>                                        |POST      |
