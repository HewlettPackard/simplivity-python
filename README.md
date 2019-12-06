[![PyPI version](https://badge.fury.io/py/simplivity.svg)](https://badge.fury.io/py/simplivity)
[![Build Status](https://travis-ci.com/HewlettPackard/simplivity-python.svg?branch=master)](https://travis-ci.com/HewlettPackard/simplivity-python-sdk)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/simplivity-python/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/simplivity-python?branch=master)

# HPE SimpliVity SDK for Python

This library provides a Python interface to the HPE SimpliVity REST APIs.

HPE SimpliVity is an intelligent hyperconverged platform that speeds application performance,
improves efficiency and resiliency, and backs up and restores VMs in seconds.

## Installation

### From source

Either:

```bash
$ git clone https://github.com/HewlettPackard/simplivity-python.git
$ cd simplivity-python
$ python setup.py install --user  # to install in the user directory (~/.local)
$ sudo python setup.py install    # to install globally
```

Or if using PIP:

```bash
$ git clone https://github.com/HewlettPackard/simplivity-python.git
$ cd simplivity-python
$ pip install .
```

Both installation methods work if you are using virtualenv, which you should be!

### From Pypi

```bash
$ pip install simplivity
```


## API Implementation

Status of the HPE SimpliVity REST interfaces that have been implemented in this Python library can be found in the [Wiki section](endpoints-support.md).


## SDK Documentation

The latest version of the SDK documentation can be found in the [SDK Documentation section](https://hewlettpackard.github.io/simplivity-python/index.html).

## Configuration

### JSON

Connection properties for accessing the OVC can be set in a JSON file.

Before running the samples or your own scripts, you must create the JSON file.
An example can be found at: [configuration sample](examples/config-rename.json).

Once you have created the JSON file, you can initialize the OVC client:

```python
ovc_client = OVC.from_json_file('/path/config.json')
```

:lock: Tip: Check the file permissions because the password is stored in clear-text.

### Environment Variables

Configuration can also be stored in environment variables:

```bash
# Required
export SIMPLIVITYSDK_OVC_IP='10.30.4.45'
export SIMPLIVITYSDK_USERNAME='admin'
export SIMPLIVITYSDK_PASSWORD='secret'

# Optional
export SIMPLIVITYSDK_SSL_CERTIFICATE='<path_to_cert.crt_file>'
export SIMPLIVITYSDK_CONNECTION_TIMEOUT='<connection time-out in seconds>'
```

:lock: Tip: Make sure no unauthorized person has access to the environment variables, since the password is stored in clear-text.

Once you have defined the environment variables, you can initialize the OVC client using the following code snippet:

```python
ovc_client = OVC.from_environment_variables()
```

### Dictionary

You can also set the configuration using a dictionary. As described above, for authentication you can use username/password:


```python
config = {
    "ip": "10.30.4.45",
    "credentials": {
        "username": "admin",
        "password": "secret"
    }
}

ovc_client_client = OVC(config)
```

:lock: Tip: Check the file permissions because the password is stored in clear-text.


### SSL Server Certificate

To enable the SDK to establish a SSL connection to the SimpliVity OVC, it is necessary to generate a CA certificate file containing the OVC credentials.

1. Fetch the SimpliVity OVC CA certificate.
```bash
$ openssl s_client -showcerts -host <ovc_ip> -port 443
```

2. Copy the OVC certificate wrapped with a header line and a footer line into a `<file_name>.crt` file.
```
-----BEGIN CERTIFICATE-----
... (OVC certificate in base64 PEM encoding) ...
-----END CERTIFICATE-----
```

3. Declare the CA Certificate location when creating a `config` dictionary.
```python
config = {
    "ip": "172.16.102.82",
    "credentials": {
        "username": "admin",
        "password": "secret"
    },
    "ssl_certificate": "/path/ovc_certificate.crt"
}
```

### SimpliVity Connection Timeout
By default the system timeout is used when connecting to OVC.  If you want to change this,
then the timeout can be set by either:

1. Setting the appropriate environment variable:
```bash
export SIMPLIVITYSDK_CONNECTION_TIMEOUT='<connection time-out in seconds>'
```

2. Setting the time-out in the JSON configuration file using the following syntax:
```json
"timeout": <timeout in seconds>
```

## Contributing and feature requests

**Contributing:** We welcome your contributions to the Python SDK for HPE SimpliVity. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

**Feature Requests:** If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.

#### Testing

When contributing code to this project, we require tests to accompany the code being delivered.
That ensures a higher standing of quality, and also helps to avoid minor mistakes and future regressions.

When writing the unit tests, the standard approach we follow is to use the python library [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) to patch all calls that would be made to the OVC and return mocked values.

We have packaged everything required to verify if the code is passing the tests in a tox file.
The tox call runs all unit tests against Python 3, runs a flake8 validation, and generates the test coverage report.

To run it, use the following command:

```
$ tox
```

You can also check out examples of tests for different resources in the [tests](tests) folder.

## License

This project is licensed under the Apache license. Please see [LICENSE](LICENSE) for more information.

## Version and changes

To view history and notes for this version, view the [Changelog](CHANGELOG.md).
