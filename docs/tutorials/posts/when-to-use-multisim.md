---
draft: true 
date: 2025-09-19 
authors:
  - gilesknight
categories:
  - Tutorials
readtime: 10
---

# When to use `MultiSim`

When faced with running many permutations of a simulation, using 
`MultiSim`' to run GLM in parallel across all available CPU cores would 
appear to be a no-brainer. 
However, running many separate processes does not always translate into 
a faster net execution time, and in some cases, actively harm it.
This tutorial will guide you through when to use `MultiSim` and when to 
avoid it.

<!-- more -->

