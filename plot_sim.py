import matplotlib.pyplot as plt

from glmpy import plots
from glmpy.example_sims import SparklingSim


sparkling = SparklingSim()
sparkling.run()

nc = plots.NCProfile(sparkling.get_sim_dir() + "/output/output.nc")
fig, ax = plt.subplots(figsize=(10, 5))
out = nc.plot_var(ax=ax, var="temp", reference="surface")
col_bar = fig.colorbar(out)
col_bar.set_label("Temperature (°C)")
fig.savefig("nc_profile.png", dpi=400)