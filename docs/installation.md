# Install

## Quick start

Install glm-py with `pip`:

``` 
pip install glmpy
```

### Built distribution (recommended)

The built distribution of glm-py comes bundled with the GLM binary. 
`pip` will automatically download the built distribution of glm-py providing:

- You have CPython 3.9-3.12 or PyPy 3.9-3.10 installed 
- You are running one of the supported OS/architectures listed in the table below

|             | Linux       | Macos       | Windows     |
| ----------- | ----------- | ----------- | ----------- |
| **x86_64**  | ✅          | ✅          | ✅           |
| **ARM64**   | ✅          | ✅          | ❌           |

### Source distribution

In the event your system does not meet the above requirements, `pip` will install the source distribution. **The source distribution does not ship with the GLM binary**. You will still be able to use glm-py (e.g., to create `.nml` files) but the package will raise an error when you call the `glm_run()` method from the `simulation.GLMSim` class.

To run GLM, you will either need to source a pre-compiled binary or [compile GLM yourself](https://github.com/AquaticEcoDynamics/GLM/tree/cc497b83a0726231d386b98d19407d0e294b116a). The `glm_path` parameter of the `glm_run()` method can be used to tell glm-py where to run the binary from.

## Release history

The following table lists the GLM version that is bundled with the built distribution of each glm-py release:


| glm-py version | GLM version |
| -------------- | ----------- |
| `0.0.1`        | `3.3.1`     |
