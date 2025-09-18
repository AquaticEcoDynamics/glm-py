# Install

## Quick start

Install glm-py with `pip`:

``` 
pip install glm-py
```

!!! tip "Advanced"

    To install the development version of glm-py use:

    ```
    pip install git+https://github.com/AquaticEcoDynamics/glm-py.git@next-release#egg=glm-py
    ```

    Note, no GLM binary is included in the development version.


### Built distribution (recommended)

The built distribution of glm-py comes bundled with the GLM binary. 
`pip` will automatically download the built distribution of glm-py providing:

- You have CPython 3.9-3.12 or PyPy 3.9-3.10 installed 
- You are running one of the supported OS/architectures listed in the table below

|             | Linux       | Macos       | Windows     |
| ----------- | ----------- | ----------- | ----------- |
| **x86_64**  | ✅          | ✅          | ❌           |
| **ARM64**   | ✅          | ✅          | ❌           |

### Source distribution

In the event your system does not meet the above requirements, `pip` will install the source distribution. **The source distribution does not ship with the GLM binary**. You will still be able to use glm-py but the package will raise an error when you call the `run()` method from of `GLMSim` or `MultiSim`.

To run GLM, you will either need to source a pre-compiled binary or [compile GLM yourself](https://github.com/AquaticEcoDynamics/GLM/tree/cc497b83a0726231d386b98d19407d0e294b116a). Use the `glm_path` parameter of `run()` to tell glm-py where to your own binary.

## Release history

The following table lists the GLM version that is bundled with the built distribution of each glm-py release:

| glm-py version | GLM version     |
| -------------- | -----------     |
| `0.5.*`        | `3.3.3`         |
| `0.4.*`        | `3.3.1a12`      |
| `0.3.*`        | `3.3.1a12`      |
| `0.2.*`        | `3.3.1a12`      |
| `0.1.*`        | `3.3.1a12`      |
