
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] 

### Added
    - endpoint support for /backups/delete <POST>
    - endpoint support for /backups/set_retention <POST>
    - endpoint support for /backups/{bkpId} <DELETE>
    - endpoint support for /backups/{bkpId}/cancel <POST>
    - endpoint support for /backups/{bkpId}/lock <POST>
    - endpoint support for /backups/{bkpId}/copy <POST>
    - endpoint support for /backups/{bkpId}/rename <POST>
    - endpoint support for /backups/{bkpId}/restore <POST>
    - endpoint support for /cluster_groups <GET>
    - endpoint support for /cluster_groups/{clusterGroupId}/rename <POST>
    - endpoint support for /datastore <POST>
    - endpoint support for /datastore/{datastoreId} <DELETE>
    - endpoint support for /datastore/{datastoreId}/resize <POST>
    - endpoint support for /datastore/{datastoreId}/set_policy <POST>
    - endpoint support for /datastore/{datastoreId}/standard_hosts <GET>
    - endpoint support for /external_stores <GET>
    - endpoint support for /hosts/{hostId}/cancel_virtual_controller_shutdown <POST>
    - endpoint support for /hosts/{hostId}/remove_from_federation <POST>    
    - endpoint support for /hosts/{hostId}/shutdown_virtual_controller <POST>
    - endpoint support for /hosts/{hostId}/hardware <GET>
    - endpoint support for /hosts/{hostId}/virtual_controller_shutdown_status <GET>
    - endpoint support for /omnistack_clusters/time_zone_list <GET>
    - endpoint support for /omnistack_clusters/{clusterId}/connected_clusters  <GET>
    - endpoint support for /omnistack_clusters/{clusterId}/set_time_zone <POST>
    - endpoint support for /omnistack_clusters/{clusterId}/throughput <GET>
    - endpoint support for /policies <POST>
    - endpoint support for /policies/resume <POST>
    - endpoint support for /policies/suspend <POST>
    - endpoint support for /policies/{policyId} <DELETE>
    - endpoint support for /policies/{policyId}/impact_report/create_rules <POST>
    - endpoint support for /policies/{policyId}/impact_report/edit_rules <POST>
    - endpoint support for /policies/{policyId}/rename <POST>
    - endpoint support for /policies/{policyId}/rules <POST>
    - endpoint support for /policies/{policyId}/rules/{ruleId} <GET>
    - endpoint support for /policies/{policyId}/rules/{ruleId} <DELETE>
    - endpoint support for /policies/{policyId}/rules/{ruleId} <PUT>
    - endpoint support for /security/certificates <GET>
    - endpoint support for /virtual_machines/{vmId}/power_off <POST>
    - endpoint support for /virtual_machines/{vmId}/power_on <POST>
    - endpoint support for /virtual_machines/policy_impact_report/apply_policy <POST>
    - missing connection unit tests to improve code coverage
    - missing ovc client host unit tests to improve code coverage
    - pull request template to facilitate pull requests
    - query string support for post operations

### Changed
    - address unittest.assertequals deprecation warning within unit test cases
    - default accept header to application/json
    - default value assigned to custom_header parameter 
    - leverage pprint in the ./examples/datastores.py to improve the overall readability of the output
    - policy test cases to improve the existing code coverage metrics
    - reformat existing docstrings to conform to Sphinx documentation requirements
    - rename the unit test filenames to reflect which objects were being targeted
    - static ip address within a unit test to the loopback ip address

### Fixed
    - exception handling within the ovc client module
    - obtain access token when 'invalid_token' reached
    - remove the caching the http.client.HTTPSConnection object
    - required __init__.py files to support unit test discovery
    - resolve failing unit test cases
    - resolve the virtual machine `__refresh` method
    - url encode query string to support values that contain spaces
    - resolve `do_get` method to append filters to uri

### Removed
    - external test dependency for mock module    

## [v1.0.0] - 2019-12-04

### Added
    - endpoint support for /backups <GET>
    - endpoint support for /datastores <GET>
    - endpoint support for /hosts <GET>
    - endpoint support for /omnistack_clusters <GET>
    - endpoint support for /policies <GET>
    - endpoint support for /virutal_machines <GET>
    - endpoint support for /virutal_machines/set_policy <POST>
    - endpoint support for /virutal_machines/{vmId} <GET>
    - endpoint support for /virutal_machines/{vmId}/backup <POST>
    - endpoint support for /virutal_machines/{vmId}/backup_parameters <POST>
    - endpoint support for /virutal_machines/{vmId}/backups <GET>
    - endpoint support for /virutal_machines/{vmId}/clone <POST>
    - endpoint support for /virutal_machines/{vmId}/move <POST>
    - endpoint support for /virutal_machines/{vmId}/set_policy <POST>
