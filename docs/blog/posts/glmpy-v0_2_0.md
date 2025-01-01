---
draft: false 
date: 2024-06-24
authors:
  - gknight
categories:
  - Releases
---

# glm-py `0.2.0`

**Key changes from the latest release.**

glm-py `0.2.0` reworks the `nml` module to provide more flexible tools for 
reading and writing NML files. 

<!-- more -->

## What's changed

- The `nml` module has been split into `nml` and `glm_nml` sub-modules.
- The `glm_nml` sub-module provides high-level NML tools and implements all the 
existing classes from the `nml` module in `0.1.3`.
  - Classes from `0.1.3` are automatically imported using 
  `from glmpy import nml` to maintain backwards compatibility until `1.0.0`.
  - Class names from `0.1.3` will be deprecated by `1.0.0` in favour of a new 
  naming convention that ensures forwards compatibility with AED. Warnings are 
  raised to encourage you to migrate to the new class names.
- The new `nml` sub-module provides low-level tools for reading and writing any
NML file (GLM or AED).
  - `NMLWriter` converts a nested Python dictionary to an NML file. 
  - `NMLReader` converts an NML file to a nested Python dictionary. 
  - Both classes provide functionality to explicitly control how each parameter
  is read/written to file.
- `InvertedTruncatedCone` class added to the `dimensions` module to calculate
morphometry parameters for simple circular water bodies.