from setuptools import Extension, setup

import versioneer

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

