# Contributing

  [aed-group]: https://github.com/AquaticEcoDynamics
  [open-issue]: https://github.com/WET-tool/glm-py/issues/new

glm-py is an open source project that is actively maintained by the [Aquatic 
EcoDynamics research group][aed-group] at the University of Western Australia.
If you'd like to contribute to the project, please familiarise yourself with
the contributing guide below.

## Environment

A Docker container can be used to create a development environment. You can 
either build the Docker image:

```
docker build -t glm-py-dev .devcontainer
```
Or, you can develop glm-py using a dev-container.

## Code style

Code linting and formatting uses ruff and black. A script to format the glm-py 
repository can be run: `./scripts/format.sh`. 

pre-commit is used to run ruff and black. 

## Tests

<a href="https://docs.pytest.org/en/7.4.x/" target="_blank">pytest</a> is used 
for testing glm-py. 

If testing, please add tests under the `tests` directory. If you need test data 
for running tests, add them as `pytest.fixtures` in `conftest.py`. 

## Pull requests

Submit pull requests to the `next-release` branch. This is where glm-py is 
actively developed.

## Suggested contributions

- An `aed_nml` sub-module for the `nml` module that mirrors the functionality
of the `glm_nml` sub-module. 
- Parameter documentation for the `glm_nml` sub-module.
- Additional simple morphometries in the `dimensions` module.

