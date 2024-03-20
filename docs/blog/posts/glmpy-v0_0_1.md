---
draft: false 
date: 2024-03-20 
authors:
  - gknight
categories:
  - Releases
---

# glm-py `0.0.1` released! 🚀

**We're pleased to announce the first release of glm-py on pip!**

glm-py provides a Python interface to the General Lake Model (GLM) that 
abstracts away the complexity of building and running simulations. It is now
easier than ever to use GLM for research, education, and software development. 

<!-- more -->

In the first release of glm-py we've prioritised providing functionality for 
the core components of modelling a water body with GLM, i.e., writing the 
`.nml` file, preparing the model inputs, and running GLM. The `nml` module of 
glm-py lets you configure your model parameters without ever needing to open
a `.nml` file. glm-py translates parameters defined in Python dictionaries to 
the format expected by GLM. The benefits of this approach include: type hints 
for explicitly declaring expected parameter types, removal of `.nml` syntax 
errors, and raising helpful error messages to enforce parameter compliance 
(coming soon!). The `simulation` module streamlines how you prepare and run 
your simulation. glm-py can automatically create a directory of your input 
files that matches the structure expected by GLM. Running the model is as 
simple as calling `glm_run()` - no need to use the command line. These features 
make running GLM less complex and more accessible.

In addition to the writing `.nml` files and running simulations, glm-py 
provides tools to automate time consuming tasks and support the development of
web applications. For example, the `dimensions` module lets you easily 
calculate the `H` and `A` parameters for common water body morphometries.
The creation of CSV inputs is also simiplified with the `inflows` and 
`outflows` modules. Meanwhile, developers can integrate GLM into web frameworks
by leveraging classes in the `glm_json` and `simulation` modules. More useful 
functionality will follow in future releases and we'd love to hear your input
on how we can expand this toolkit.

Looking ahead, the development of glm-py is planning to incorporate:

- Complete error checking of model parameters
- A calibration module
- Expanded functionality for AED

We encourage you to use glm-py and engage with the project on GitHub. Be
sure to browse this documentation website for a complete guide on using the 
package. 

Happy modelling!


