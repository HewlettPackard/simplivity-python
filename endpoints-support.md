Refer SimpliVity REST API doc for the resource endpoints documentation [HPE SimpliVity REST API Documentation](https://developer.hpe.com/api/simplivity/).

<br />

## Supported resources and endpoints

| Endpoints                                                                               | Action   |
| --------------------------------------------------------------------------------------- | -------- |
|     **Backups**
|<sub>/backups	</sub>                                                                    |GET       |
|<sub>/backups/delete  </sub>                                                             |POST      |
|<sub>/backups/{bkpId}  </sub>                                                            |DELETE    |
|     **Datastores**
|<sub>/datastores	</sub>                                                                |GET       |
|<sub>/datastores/{datastoreId}  </sub>                                                   |DELETE    |
|     **Hosts**
|<sub>/hosts	</sub>                                                                    |GET       |
|<sub>/hosts/{hostId}/remove_from_federation  </sub>						|POST      |
|     **OmniStack Clusters**
|<sub>/omnistack_clusters	</sub>                                                        |GET       |
|     **Policies**
|<sub>/policies	</sub>                                                                    |GET       |
|<sub>/policies</sub>                                                                     |POST
|<sub>/policies/{policyId} </sub>                                                         |DELETE    |
|     **Virtual Machines**
|<sub>/virtual_machines	</sub>                                                            |GET       |
|<sub>/virtual_machines/set_policy	</sub>                                                |POST      |
|<sub>/virtual_machines/{vmId}	</sub>                                                    |GET       |
|<sub>/virtual_machines/{vmId}/backup	</sub>                                            |POST      |
|<sub>/virtual_machines/{vmId}/backup_parameters	</sub>                                |POST      |
|<sub>/virtual_machines/{vmId}/backups	</sub>                                            |GET       |
|<sub>/virtual_machines/{vmId}/clone	</sub>                                            |POST      |
|<sub>/virtual_machines/{vmId}/move	</sub>                                                |POST      |
|<sub>/virtual_machines/{vmId}/set_policy	</sub>                                        |POST      |
