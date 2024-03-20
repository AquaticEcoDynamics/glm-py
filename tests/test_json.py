import pytest
from glmpy.glm_json import JSONReader


def test_json_to_nml_invalid_json_file():
    with pytest.raises(TypeError):
        JSONReader(json_file=123, nml_file="sim.nml")


def test_json_nml_get_nml_blocks(json_nml_sparkling):
    sparkling_json = JSONReader(json_nml_sparkling, "glm3.nml")
    target_keys = set(
        [
            '&glm_setup', '&mixing', '&morphometry', '&time', '&wq_setup', 
            '&output', '&init_profiles', '&meteorology', '&bird_model', 
            '&light', '&inflows', '&outflows', '&sediment'
        ]
    )
    json_keys = set(sparkling_json.get_nml_blocks())
    
    assert target_keys == json_keys

def test_json_nml_from_dict_get_nml_parameters(json_nml_sparkling):
    sparkling_json = JSONReader(json_nml_sparkling, "glm3.nml")
    sparkling_setup_keys = list(
        sparkling_json.get_nml_parameters("&glm_setup").keys()
    )
    target_keys = [
        'sim_name', 'max_layers', 'min_layer_vol', 'min_layer_thick', 
        'max_layer_thick', 'density_model', 'non_avg'
    ]
    
    assert sparkling_setup_keys == target_keys