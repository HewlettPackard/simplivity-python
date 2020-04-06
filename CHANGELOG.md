
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] 

### Added
    - endpoint support for /backups/delete <POST>
    - endpoint support for /backups/{bkpId} <DELETE>
    - endpoint support for /datastore <POST>
    - endpoint support for /datastore/{datastoreId} <DELETE>
    - endpoint support for /hosts/{hostId}/remove_from_federation <POST>    
    - endpoint support for /policies/{policyId} <DELETE>
    - endpoint support for /policies <POST>
    - endpoint support for /virtual_machines/{vmId}/power_off <POST>
    - pull request template to facilitate pull requests
    - query string support for post operations

### Changed
    - address unittest.assertequals deprecation warning within unit test cases
    - leverage pprint in the ./examples/datastores.py to improve the overall readability of the output
    - policy test cases to improve the existing code coverage metrics
    - reformat existing docstrings to conform to Sphinx documentation requirements
    - rename the unit test filenames to reflect which objects were being targeted

### Fixed
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
	
