import pytest
import pandas as pd

from glmpy.example_sims import sparkling


def test_sparkling_load_nml():
    sparkling_dict = sparkling.load_nml()
    assert sparkling_dict["glm_setup"]["sim_name"] == "Sparkling"

def test_sparkling_load_bcs():
    bcs_pd = sparkling.load_bcs()
    assert bcs_pd["time"][0] == "1979-01-04"