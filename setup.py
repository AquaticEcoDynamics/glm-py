from setuptools import Extension, setup

import sysconfig
import versioneer

# Work around missing PyPy sysconfig var in some manylinux environments.
config_vars = sysconfig.get_config_vars()
if config_vars.get("LDCXXSHARED") is None and config_vars.get("LDSHARED"):
    config_vars["LDCXXSHARED"] = config_vars["LDSHARED"]

# see pyproject.toml for static project metadata
setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    ext_modules=[
        Extension(
            name="glmpylib.glmpy",  
            sources=["glmpy/glmpy.c"], 
        ),
    ]
)
