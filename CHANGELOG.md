
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] 

### Added
    - endpoint support for /backups/delete <POST>
    - endpoint support for /backups/{bkpId} <DELETE>
    - endpoint support for /backups/{bkpId}/restore <POST>
    - endpoint support for /cluster_groups <GET>
    - endpoint support for /datastore <POST>
    - endpoint support for /datastore/{datastoreId} <DELETE>
    - endpoint support for /datastore/{datastoreId}/resize <POST>
    - endpoint support for /datastore/{datastoreId}/set_policy <POST>
    - endpoint support for /hosts/{hostId}/remove_from_federation <POST>    
    - endpoint support for /hosts/{hostId}/hardware <GET>
    - endpoint support for /policies <POST>
    - endpoint support for /policies/{policyId} <DELETE>
    - missing ovc client host unit tests to improve code coverage
    - pull request template to facilitate pull requests
    - query string support for post operations

### Changed
    - address unittest.assertequals deprecation warning within unit test cases
    - default accept header to application/json
    - leverage pprint in the ./examples/datastores.py to improve the overall readability of the output
    - policy test cases to improve the existing code coverage metrics
    - reformat existing docstrings to conform to Sphinx documentation requirements
    - rename the unit test filenames to reflect which objects were being targeted
    - static ip address within a unit test to the loopback ip address

### Fixed
    - exception handling within the ovc client module
    - required __init__.py files to support unit test discovery
    - resolve failing unit test cases
    - url encode query string to support values that contain spaces

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
