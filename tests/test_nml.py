import json
import pytest

from glmpy.nml import nml
from glmpy.nml import glm_nml

def test_write_nml_bool():
    assert nml.NMLWriter.write_nml_bool(True) == ".true."
    assert nml.NMLWriter.write_nml_bool(False) == ".false."

def test_write_nml_str():
    python_str = 'temp'
    assert nml.NMLWriter.write_nml_str(python_str) == f"'{python_str}'"

@pytest.mark.parametrize("python_syntax, nml_syntax, converter_func", [
    ([True], ".true.", nml.NMLWriter.write_nml_bool),
    (
        [True, False, True], ".true.,.false.,.true.", 
        nml.NMLWriter.write_nml_bool
    ),
    (['temp'], f"'{'temp'}'", nml.NMLWriter.write_nml_str),
    (
        ['temp', 'salt', 'oxy'], 
        f"'{'temp'}','{'salt'}','{'oxy'}'", 
        nml.NMLWriter.write_nml_str
    ),
    ([12.3], "12.3", None),
    ([12.3, 32.4, 64.2], "12.3,32.4,64.2", None)
])

def test_write_nml_list(python_syntax, nml_syntax, converter_func):
    assert nml.NMLWriter.write_nml_list(
        python_list=python_syntax,
        converter_func=converter_func
    ) == nml_syntax

@pytest.fixture
def example_python_params():
    return {
        "param1": 123,
        "param2": 1.23,
        "param3": "foo",
        "param4": True,
        "param5": [1, 2, 3],
        "param6": [1.1, 2.1, 3.1],
        "param7": ["foo", "bar", "baz"],
        "param8": [True, False, True],
        "param9": [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
        "param10": [[1.1, 2.1, 3.1], [1.1, 2.1, 3.1], [1.1, 2.1, 3.1]],
        "param11": [
            ["foo", "bar", "baz"], ["foo", "bar", "baz"], ["foo", "bar", "baz"]
        ],
        "param12": [
            [True, False, True], [True, False, True], [True, False, True]
        ]
    }

def test_write_nml_param(example_python_params):
    assert nml.NMLWriter.write_nml_param(
        param_name="param1",
        param_value=example_python_params["param1"],
        converter_func=None
    ) == "   param1 = 123\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param2",
        param_value=example_python_params["param2"],
        converter_func=None
    ) == "   param2 = 1.23\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param3",
        param_value=example_python_params["param3"],
        converter_func=nml.NMLWriter.write_nml_str
    ) == "   param3 = 'foo'\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param4",
        param_value=example_python_params["param4"],
        converter_func=nml.NMLWriter.write_nml_bool
    ) == "   param4 = .true.\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param5",
        param_value=example_python_params["param5"],
        converter_func=nml.NMLWriter.write_nml_list
    ) == "   param5 = 1,2,3\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param6",
        param_value=example_python_params["param6"],
        converter_func=nml.NMLWriter.write_nml_list
    ) == "   param6 = 1.1,2.1,3.1\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param7",
        param_value=example_python_params["param7"],
        converter_func=lambda x: nml.NMLWriter.write_nml_list(
            x, nml.NMLWriter.write_nml_str
        )
    ) == "   param7 = 'foo','bar','baz'\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param8",
        param_value=example_python_params["param8"],
        converter_func=lambda x: nml.NMLWriter.write_nml_list(
            x, nml.NMLWriter.write_nml_bool
        )
    ) == "   param8 = .true.,.false.,.true.\n"
    assert nml.NMLWriter.write_nml_param(
        param_name="param9",
        param_value=example_python_params["param9"],
        converter_func=nml.NMLWriter.write_nml_array
    ) == (
        "   param9 = 1,2,3,\n"+
        "            1,2,3,\n"+
        "            1,2,3\n"
    )
    assert nml.NMLWriter.write_nml_param(
        param_name="param10",
        param_value=example_python_params["param10"],
        converter_func=nml.NMLWriter.write_nml_array
    ) == (
        "   param10 = 1.1,2.1,3.1,\n"+
        "             1.1,2.1,3.1,\n"+
        "             1.1,2.1,3.1\n"
    )
    assert nml.NMLWriter.write_nml_param(
        param_name="param11",
        param_value=example_python_params["param11"],
        converter_func=lambda x: nml.NMLWriter.write_nml_array(
            x, nml.NMLWriter.write_nml_str
        )
    ) == (
        "   param11 = 'foo','bar','baz',\n"+
        "             'foo','bar','baz',\n"+
        "             'foo','bar','baz'\n"
    )
    assert nml.NMLWriter.write_nml_param(
        param_name="param12",
        param_value=example_python_params["param12"],
        converter_func=lambda x: nml.NMLWriter.write_nml_array(
            x, nml.NMLWriter.write_nml_bool
        )
    ) == (
        "   param12 = .true.,.false.,.true.,\n"+
        "             .true.,.false.,.true.,\n"+
        "             .true.,.false.,.true.\n"
    )

@pytest.fixture
def example_glm_setup_parameters():
    return {
        "sim_name": "Example Simulation #1",
        "max_layers": 500,
        "min_layer_thick": 0.15,
        "max_layer_thick": 1.50,
        "min_layer_vol": 0.025,
        "density_model": 1,
        "non_avg": False
    }

@pytest.fixture
def example_mixing_parameters():
    return {
        "surface_mixing": 1,
        "coef_mix_conv": 0.125,
        "coef_wind_stir": 0.23,
        "coef_mix_shear":0.2,
        "coef_mix_turb": 0.51,
        "coef_mix_KH": 0.3,
        "deep_mixing": 2,
        "coef_mix_hyp": 0.5,
        "diff": 0.0
    }

@pytest.fixture
def example_wq_setup_parameters():
    return {
        "wq_lib":"aed2",
        "wq_nml_file": "aed2/aed2.nml",
        "ode_method": 1,
        "split_factor": 1,
        "bioshade_feedback": True,
        "repair_state": True,
        "mobility_off": False
    }

@pytest.fixture
def example_morphometry_parameters():
    return {
        "lake_name":'Example Lake',
        "latitude": 32.0,
        "longitude": 35.0,
        "base_elev": -252.9,
        "crest_elev": -203.9,
        "bsn_len": 21000.0,
        "bsn_wid": 13000.0,
        "bsn_vals": 45,
        "H": [
            -252.9, -251.9, -250.9, -249.9, -248.9, -247.9, -246.9, -245.9, 
            -244.9, -243.9, -242.9, -241.9, -240.9, -239.9, -238.9, -237.9, 
            -236.9, -235.9, -234.9, -233.9, -232.9, -231.9, -230.9, -229.9,  
            -228.9, -227.9, -226.9, -225.9, -224.9, -223.9, -222.9, -221.9,  
            -220.9, -219.9, -218.9, -217.9, -216.9, -215.9, -214.9, -213.9,  
            -212.9, -211.9, -208.9, -207.9, -203.9
        ],
        "A": [
            0, 9250000, 15200000, 17875000, 21975000, 26625000, 31700000, 
            33950000, 38250000, 41100000, 46800000, 51675000, 55725000, 
            60200000, 64675000, 69600000, 74475000, 79850000, 85400000, 
            90975000, 96400000, 102000000, 107000000, 113000000, 118000000, 
            123000000, 128000000, 132000000, 136000000, 139000000, 143000000, 
            146000000, 148000000, 150000000, 151000000, 153000000, 155000000, 
            157000000, 158000000, 160000000, 161000000, 162000000, 167000000, 
            170000000, 173000000
        ]
    }

@pytest.fixture
def example_time_parameters():
    return {
        "timefmt": 3,
        "start": "1997-01-01 00:00:00",
        "stop": "1999-01-01 00:00:00",
        "dt": 3600.0,
        "num_days": 730,
        "timezone": 7.0
    }

@pytest.fixture
def example_output_parameters():
    return {
        'out_dir': 'output',
        'out_fn': 'output',
        'nsave': 6,
        'csv_lake_fname': 'lake',
        'csv_point_nlevs': 2,
        'csv_point_fname': 'WQ_' ,
        "csv_point_frombot": [1], 
        'csv_point_at': [5, 30],    
        'csv_point_nvars': 7,
        'csv_point_vars': [
            'temp', 'salt', 'OXY_oxy', 'SIL_rsi', 
            'NIT_amm', 'NIT_nit', 'PHS_frp'
        ],
        'csv_outlet_allinone': False,
        'csv_outlet_fname': 'outlet_',
        'csv_outlet_nvars': 4,
        'csv_outlet_vars': ['flow', 'temp', 'salt', 'OXY_oxy'],
        'csv_ovrflw_fname': "overflow"
    }

@pytest.fixture
def example_init_profiles_parameters():
    return {
        "lake_depth": 43,
        "num_depths": 3,
        "the_depths": [1, 20, 40],
        "the_temps": [18.0, 18.0, 18.0],
        "the_sals": [ 0.5, 0.5, 0.5],
        "num_wq_vars": 6,
        "wq_names": [
            'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc','OGM_poc'
        ],
        "wq_init_vals": [
            [1.1, 1.2, 1.3, 1.2, 1.3],
            [2.1, 2.2, 2.3, 1.2, 1.3],
            [3.1, 3.2, 3.3, 1.2, 1.3],
            [4.1, 4.2, 4.3, 1.2, 1.3],
            [5.1, 5.2, 5.3, 1.2, 1.3],
            [6.1, 6.2, 6.3, 1.2, 1.3]
        ]
    }

@pytest.fixture
def example_light_parameters():
    return {
        "light_mode": 0,
        "Kw": 0.4,
        "n_bands": 4,
        "light_extc": [1.0, 0.5, 2.0, 4.0],
        "energy_frac": [0.51, 0.45, 0.035, 0.005],
        "Benthic_Imin": 10
    }

@pytest.fixture
def example_bird_model_parameters():
    return {
        "AP": 973,
        "Oz": 0.279,
        "WatVap": 1.1,
        "AOD500": 0.033,
        "AOD380": 0.038,
        "Albedo": 0.2
    }

@pytest.fixture
def example_sediment_parameters():
    return {
        "sed_heat_Ksoil":0.0,
        "sed_temp_depth": 0.2,
        "sed_temp_mean": [5, 10, 20],
        "sed_temp_amplitude": [6, 8, 10],
        "sed_temp_peak_doy": [80, 70, 60],
        "benthic_mode": 1,
        "n_zones": 3,
        "zone_heights": [10.0, 20.0, 50.0],
        "sed_reflectivity": [0.1, 0.01, 0.01],
        "sed_roughness": [0.1, 0.01, 0.01]
    }

@pytest.fixture
def example_snow_ice_parameters():
    return {
        "snow_albedo_factor":1.0,
        "snow_rho_min": 50,
        "snow_rho_max": 300
    }

@pytest.fixture
def example_meteorology_parameters():
    return {
        "met_sw": True,
        "lw_type": "LW_IN",
        "rain_sw": False,
        "atm_stab": 0,
        "fetch_mode": 0,
        "rad_mode": 1,
        "albedo_mode": 1,
        "cloud_mode": 4,
        "subdaily": True,
        "meteo_fl": 'bcs/met_hourly.csv',
        "wind_factor": 0.9,
        "ce": 0.0013,
        "ch": 0.0013,
        "cd": 0.0013,
        "catchrain": True,
        "rain_threshold": 0.001,
        "runoff_coef": 0.0,
    }

@pytest.fixture
def example_inflow_parameters():
    return {
        "num_inflows": 6,
        "names_of_strms": [
            'Inflow1','Inflow2','Inflow3','Inflow4','Inflow5','Inflow6'
            ],
        "subm_flag": [False, False, False, True, False, False],
        "strm_hf_angle": [85.0, 85.0, 85.0, 85.0, 85.0, 85.0],
        "strmbd_slope": [4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
        "strmbd_drag": [0.0160, 0.0160, 0.0160, 0.0160, 0.0160, 0.0160],
        "inflow_factor": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "inflow_fl": [
            'bcs/inflow_1.csv', 'bcs/inflow_2.csv', 'bcs/inflow_3.csv', 
            'bcs/inflow_4.csv', 'bcs/inflow_5.csv', 'bcs/inflow_6.csv'
        ],
        "inflow_varnum": 3,
        "inflow_vars": ['FLOW', 'TEMP', 'SALT'],
        "coef_inf_entrain": 0.0,
        "time_fmt": 'YYYY-MM-DD hh:mm:ss'
    }

@pytest.fixture
def example_outflow_parameters():
    return {
        "num_outlet": 1,
        "flt_off_sw": False,
        "outlet_type": 1,
        "outl_elvs": -215.5,
        "bsn_len_outl": 18000,
        "bsn_wid_outl": 11000,
        "outflow_fl" : 'bcs/outflow.csv',
        "outflow_factor": 1.0,
        "seepage": True,
        "seepage_rate": 0.01,
    }

def test_write_nml(
        tmp_path,
        example_glm_setup_parameters,
        example_mixing_parameters,
        example_morphometry_parameters,
        example_time_parameters,
        example_output_parameters,
        example_init_profiles_parameters,
        example_meteorology_parameters,
        example_light_parameters,
        example_bird_model_parameters,
        example_inflow_parameters,
        example_outflow_parameters,
        example_sediment_parameters,
        example_snow_ice_parameters,
        example_wq_setup_parameters
):
    glm_setup = glm_nml.SetupBlock()
    morphometry = glm_nml.MorphometryBlock()
    time = glm_nml.TimeBlock()
    init_profiles = glm_nml.InitProfilesBlock()
    mixing = glm_nml.MixingBlock()
    output = glm_nml.OutputBlock()
    meteorology = glm_nml.MeteorologyBlock()
    light = glm_nml.LightBlock()
    bird_model = glm_nml.BirdModelBlock()
    inflow = glm_nml.InflowBlock()
    outflow = glm_nml.OutflowBlock()
    sediment = glm_nml.SedimentBlock()
    snow_ice = glm_nml.SnowIceBlock()
    wq_setup = glm_nml.WQSetupBlock()

    glm_setup.set_attrs(example_glm_setup_parameters)
    morphometry.set_attrs(example_morphometry_parameters)
    time.set_attrs(example_time_parameters)
    init_profiles.set_attrs(example_init_profiles_parameters)
    mixing.set_attrs(example_mixing_parameters)
    output.set_attrs(example_output_parameters)
    meteorology.set_attrs(example_meteorology_parameters)
    light.set_attrs(example_light_parameters)
    bird_model.set_attrs(example_bird_model_parameters)
    inflow.set_attrs(example_inflow_parameters)
    outflow.set_attrs(example_outflow_parameters)
    sediment.set_attrs(example_sediment_parameters)
    snow_ice.set_attrs(example_snow_ice_parameters)
    wq_setup.set_attrs(example_wq_setup_parameters)

    nml_file = glm_nml.GLMNML(
        glm_setup=glm_setup.get_params(),
        morphometry=morphometry.get_params(),
        time=time.get_params(),
        init_profiles=init_profiles.get_params(),
        mixing=mixing.get_params(),
        output=output.get_params(),
        meteorology=meteorology.get_params(),
        light=light.get_params(),
        bird_model=bird_model.get_params(),
        inflow=inflow.get_params(),
        outflow=outflow.get_params(),
        sediment=sediment.get_params(),
        snow_ice=snow_ice.get_params(),
        wq_setup=wq_setup.get_params(),
        check_params=False
    )
    file_path = tmp_path / "test.nml"
    nml_file.write_nml(file_path)

    with open(file_path, "r") as file:
        content = file.read()
    
    expected = (
        "&glm_setup\n" +
        "   sim_name = 'Example Simulation #1'\n" +
        "   max_layers = 500\n" +
        "   min_layer_vol = 0.025\n" +
        "   min_layer_thick = 0.15\n" +
        "   max_layer_thick = 1.5\n" +
        "   density_model = 1\n" +
        "   non_avg = .false.\n" +
        "/" + 
        "\n" +
        "&mixing\n" +
        "   surface_mixing = 1\n" +
        "   coef_mix_conv = 0.125\n" +
        "   coef_wind_stir = 0.23\n" +
        "   coef_mix_shear = 0.2\n" +
        "   coef_mix_turb = 0.51\n" +
        "   coef_mix_KH = 0.3\n" +
        "   deep_mixing = 2\n" +
        "   coef_mix_hyp = 0.5\n" +
        "   diff = 0.0\n" +
        "/" +
        "\n" +
        "&morphometry\n" +
        "   lake_name = 'Example Lake'\n" +
        "   latitude = 32.0\n" +
        "   longitude = 35.0\n" +
        "   base_elev = -252.9\n" +
        "   crest_elev = -203.9\n" +
        "   bsn_len = 21000.0\n" +
        "   bsn_wid = 13000.0\n" +
        "   bsn_vals = 45\n" +
        "   H = -252.9,-251.9,-250.9,-249.9,-248.9,-247.9,-246.9,-245.9," +
        "-244.9,-243.9,-242.9,-241.9,-240.9,-239.9,-238.9,-237.9," +
        "-236.9,-235.9,-234.9,-233.9,-232.9,-231.9,-230.9,-229.9," + 
        "-228.9,-227.9,-226.9,-225.9,-224.9,-223.9,-222.9,-221.9," + 
        "-220.9,-219.9,-218.9,-217.9,-216.9,-215.9,-214.9,-213.9," + 
        "-212.9,-211.9,-208.9,-207.9,-203.9\n"
        "   A = 0,9250000,15200000,17875000,21975000,26625000,31700000," +
            "33950000,38250000,41100000,46800000,51675000,55725000," +
            "60200000,64675000,69600000,74475000,79850000,85400000," +
            "90975000,96400000,102000000,107000000,113000000,118000000," +
            "123000000,128000000,132000000,136000000,139000000,143000000," +
            "146000000,148000000,150000000,151000000,153000000,155000000," +
            "157000000,158000000,160000000,161000000,162000000,167000000," +
            "170000000,173000000\n" +
        "/" +
        "\n" +
        "&time\n" +
        "   timefmt = 3\n" +
        "   start = '1997-01-01 00:00:00'\n" +
        "   stop = '1999-01-01 00:00:00'\n" +
        "   dt = 3600.0\n" +
        "   num_days = 730\n" +
        "   timezone = 7.0\n" +
        "/" +
        "\n" +
        "&output\n" +
        "   out_dir = 'output'\n" +
        "   out_fn = 'output'\n" +
        "   nsave = 6\n" +
        "   csv_lake_fname = 'lake'\n" +
        "   csv_point_nlevs = 2\n" +
        "   csv_point_fname = 'WQ_'\n" +
        "   csv_point_frombot = 1\n" +
        "   csv_point_at = 5,30\n" +
        "   csv_point_nvars = 7\n" +
        "   csv_point_vars = 'temp','salt','OXY_oxy','SIL_rsi','NIT_amm'," +
        "'NIT_nit','PHS_frp'\n" +
        "   csv_outlet_allinone = .false.\n" +
        "   csv_outlet_fname = 'outlet_'\n" +
        "   csv_outlet_nvars = 4\n" +
        "   csv_outlet_vars = 'flow','temp','salt','OXY_oxy'\n" +
        "   csv_ovrflw_fname = 'overflow'\n" + 
        "/" + 
        "\n"+
        "&init_profiles\n" +
        "   lake_depth = 43\n" +
        "   num_depths = 3\n" +
        "   the_depths = 1,20,40\n" +
        "   the_temps = 18.0,18.0,18.0\n" +
        "   the_sals = 0.5,0.5,0.5\n" +
        "   num_wq_vars = 6\n" +
        "   wq_names = 'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc'," +
        "'OGM_poc'\n" +
        "   wq_init_vals = 1.1,1.2,1.3,1.2,1.3,\n" +
        "                  2.1,2.2,2.3,1.2,1.3,\n" +
        "                  3.1,3.2,3.3,1.2,1.3,\n" +
        "                  4.1,4.2,4.3,1.2,1.3,\n" +
        "                  5.1,5.2,5.3,1.2,1.3,\n" +
        "                  6.1,6.2,6.3,1.2,1.3\n" +
        "/" +
        "\n" +
        "&meteorology\n" +
        "   met_sw = .true.\n" +
        "   meteo_fl = 'bcs/met_hourly.csv'\n" +
        "   subdaily = .true.\n" +
        "   rad_mode = 1\n" +
        "   albedo_mode = 1\n" +
        "   lw_type = 'LW_IN'\n" +
        "   cloud_mode = 4\n" +
        "   atm_stab = 0\n" +
        "   ce = 0.0013\n" +
        "   ch = 0.0013\n" +
        "   rain_sw = .false.\n" +
        "   catchrain = .true.\n" +
        "   rain_threshold = 0.001\n" +
        "   runoff_coef = 0.0\n" +
        "   cd = 0.0013\n" +
        "   wind_factor = 0.9\n" +
        "   fetch_mode = 0\n" +
        "/" +
        "\n" +
        "&light\n" +
        "   light_mode = 0\n" +
        "   Kw = 0.4\n" +
        "   n_bands = 4\n" +
        "   light_extc = 1.0,0.5,2.0,4.0\n" +
        "   energy_frac = 0.51,0.45,0.035,0.005\n" +
        "   Benthic_Imin = 10\n" +
        "/" +
        "\n" +
        "&bird_model\n" +
        "   AP = 973\n" +
        "   Oz = 0.279\n" +
        "   WatVap = 1.1\n" +
        "   AOD500 = 0.033\n" +
        "   AOD380 = 0.038\n" +
        "   Albedo = 0.2\n" +
        "/" +
        "\n" +
        "&inflow\n" +
        "   num_inflows = 6\n" +
        "   names_of_strms = 'Inflow1','Inflow2','Inflow3','Inflow4',"+
        "'Inflow5','Inflow6'\n" +
        "   subm_flag = .false.,.false.,.false.,.true.,.false.,.false.\n" +
        "   strm_hf_angle = 85.0,85.0,85.0,85.0,85.0,85.0\n" +
        "   strmbd_slope = 4.0,4.0,4.0,4.0,4.0,4.0\n" +
        "   strmbd_drag = 0.016,0.016,0.016,0.016,0.016,0.016\n" +
        "   coef_inf_entrain = 0.0\n" +
        "   inflow_factor = 1.0,1.0,1.0,1.0,1.0,1.0\n" +
        "   inflow_fl = 'bcs/inflow_1.csv','bcs/inflow_2.csv'," +
        "'bcs/inflow_3.csv','bcs/inflow_4.csv','bcs/inflow_5.csv'," + 
        "'bcs/inflow_6.csv'\n" +
        "   inflow_varnum = 3\n" +
        "   inflow_vars = 'FLOW','TEMP','SALT'\n" +
        "   time_fmt = 'YYYY-MM-DD hh:mm:ss'\n" +
        "/" +
        "\n" +
        "&outflow\n" +
        "   num_outlet = 1\n" +
        "   outflow_fl = 'bcs/outflow.csv'\n" +
        "   outflow_factor = 1.0\n" +
        "   flt_off_sw = .false.\n" +
        "   outlet_type = 1\n" +
        "   outl_elvs = -215.5\n" +
        "   bsn_len_outl = 18000\n" +
        "   bsn_wid_outl = 11000\n" +
        "   seepage = .true.\n" +
        "   seepage_rate = 0.01\n" +
        "/" +
        "\n" +
        "&sediment\n" +
        "   sed_heat_Ksoil = 0.0\n" +
        "   sed_temp_depth = 0.2\n" +
        "   sed_temp_mean = 5,10,20\n" +
        "   sed_temp_amplitude = 6,8,10\n" +
        "   sed_temp_peak_doy = 80,70,60\n" +
        "   benthic_mode = 1\n" +
        "   n_zones = 3\n" +
        "   zone_heights = 10.0,20.0,50.0\n" +
        "   sed_reflectivity = 0.1,0.01,0.01\n" +
        "   sed_roughness = 0.1,0.01,0.01\n" +
        "/" +
        "\n" +
        "&snowice\n" +
        "   snow_albedo_factor = 1.0\n" +
        "   snow_rho_min = 50\n" +
        "   snow_rho_max = 300\n" +
        "/" +
        "\n" +
        "&wq_setup\n" +
        "   wq_lib = 'aed2'\n" +
        "   wq_nml_file = 'aed2/aed2.nml'\n" +
        "   bioshade_feedback = .true.\n" +
        "   mobility_off = .false.\n" +
        "   ode_method = 1\n" +
        "   split_factor = 1\n" +
        "   repair_state = .true.\n" +
        "/" +
        "\n" 
    )
    assert content == expected

@pytest.fixture
def example_nml_parameters():
    return {
        "nml_bool_1": ".true.",
        "nml_bool_2": ".false.",
        "nml_bool_3": ".TRUE.",
        "nml_bool_4": ".FALSE.",
        "nml_int_1": "123",
        "nml_float_1": "1.23",
        "nml_str_1": "'foo'",
        "nml_str_2": '"foo"',
        "nml_list_1": "'foo', 'bar', 'baz'",
        "nml_list_2": "1, 2, 3",
        "nml_list_3": "1.1, 2.1, 3.1",
        "nml_list_4": ".true., .false., .TRUE., .FALSE.",
        "nml_array_1": ["1, 2, 3", "4, 5, 6"],
        "nml_array_2": ["1.1, 2.1, 3.1", "1.2, 2.2, 3.2"],
        "nml_array_3": ["'foo', 'bar', 'baz'", '"foo", "bar", "baz"'],
        "nml_array_4": [".true., .FALSE.", ".TRUE., .false."]
    }

def test_read_nml_methods(example_nml_parameters):
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_1"]
    ) is True
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_2"]
    ) is False
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_3"]
    ) is True
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_4"]
    ) is False
    assert nml.NMLReader.read_nml_int(
        nml_int=example_nml_parameters["nml_int_1"]
    ) == 123
    assert nml.NMLReader.read_nml_float(
        nml_float=example_nml_parameters["nml_float_1"]
    ) == 1.23
    assert nml.NMLReader.read_nml_str(
        nml_str=example_nml_parameters["nml_str_1"]
    ) == "foo"
    assert nml.NMLReader.read_nml_str(
        nml_str=example_nml_parameters["nml_str_2"]
    ) == "foo"
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_1"],
        converter_func=nml.NMLReader.read_nml_str
    ) == ["foo", "bar", "baz"]
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_2"],
        converter_func=nml.NMLReader.read_nml_int
    ) == [1, 2, 3]
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_3"],
        converter_func=nml.NMLReader.read_nml_float
    ) == [1.1, 2.1, 3.1]
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_4"],
        converter_func=nml.NMLReader.read_nml_bool
    ) == [True, False, True, False]
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_1"],
        converter_func=nml.NMLReader.read_nml_int
    ) == [[1, 2, 3], [4, 5, 6]]
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_2"],
        converter_func=nml.NMLReader.read_nml_float
    ) == [[1.1, 2.1, 3.1], [1.2, 2.2, 3.2]] 
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_3"],
        converter_func=nml.NMLReader.read_nml_str
    ) == [['foo', 'bar', 'baz'], ["foo", "bar", "baz"]]
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_4"],
        converter_func=nml.NMLReader.read_nml_bool
    ) == [[True, False], [True, False]]

def test_read_nml_int_exceptions():
    with pytest.raises(TypeError) as error:
        input = 123
        nml.NMLReader.read_nml_int(input)
    assert str(error.value) == (
        f"Expected a string but got type: {type(input)}."
    )
    with pytest.raises(ValueError) as error:
        input = "foo"
        nml.NMLReader.read_nml_int(input)
    assert str(error.value) == (
        f"Unable to convert '{input}' to an integer."
    )

def test_read_nml_float_exceptions():
    with pytest.raises(TypeError) as error:
        input = 1.23
        nml.NMLReader.read_nml_float(input)
    assert str(error.value) == (
        f"Expected a string but got type: {type(input)}."
    )
    with pytest.raises(ValueError) as error:
        input = "foo"
        nml.NMLReader.read_nml_float(input)
    assert str(error.value) == (
        f"Unable to convert '{input}' to a float."
    )

def test_read_nml_bool_exceptions():
    with pytest.raises(TypeError) as error:
        input = True
        nml.NMLReader.read_nml_bool(input)
    assert str(error.value) == (
        f"Expected a string but got type: {type(input)}."
    )
    with pytest.raises(ValueError) as error:
        input = "foo"
        nml.NMLReader.read_nml_bool(input)
    assert str(error.value) == (
        f"Expected a single NML boolean but got '{input}'. "
        "Valid NML boolean strings are '.true.', '.TRUE.', '.false.', "
        "or '.FALSE.'."
    )

def test_read_nml_str_exceptions():
    with pytest.raises(TypeError) as error:
        input = 123
        nml.NMLReader.read_nml_str(input)
    assert str(error.value) == (
        f"Expected a string but got type: {type(input)}."
    )

def test_read_nml_list_exceptions():
    with pytest.raises(TypeError) as error:
        input = 123
        nml.NMLReader.read_nml_list(input, nml.NMLReader.read_nml_int)
    assert str(error.value) == (
        f"Expected a string or a list but got type: {type(input)}."
    )
    with pytest.raises(TypeError) as error:
        input = "foo"
        converter_func = "foo"
        nml.NMLReader.read_nml_list(input, converter_func)
    assert str(error.value) == (
        f"Expected a Callable but got type: {type(converter_func)}."
    )
    with pytest.raises(TypeError) as error:
        input = ["foo, baz, bar", 123]
        converter_func = nml.NMLReader.read_nml_str
        nml.NMLReader.read_nml_list(input, converter_func)
    assert str(error.value) == (
        f"Expected a string for item {1} of nml_list but got "
        f"type: {type(input[1])}"
    )

def test_read_nml_array_exceptions():
    with pytest.raises(TypeError) as error:
        input = 123
        nml.NMLReader.read_nml_array(input, nml.NMLReader.read_nml_int)
    assert str(error.value) == (
        f"Expected a list but got type: {type(input)}."
    )
    with pytest.raises(TypeError) as error:
        input = ["1.1, 1.2, 1.3", "2.1, 2.2, 2.3"]
        converter_func = "foo"
        nml.NMLReader.read_nml_array(input, converter_func)
    assert str(error.value) == (
        f"Expected a Callable but got type: {type(converter_func)}."
    )
    with pytest.raises(TypeError) as error:
        input = ["1.1, 1.2, 1.3", 123]
        converter_func = nml.NMLReader.read_nml_float
        nml.NMLReader.read_nml_array(input, converter_func)
    assert str(error.value) == (
        f"Expected a string for item {1} of nml_array but got "
        f"type: {type(input[1])}"
    )

def test_NMLReader_get_block_valid(ellenbrook_nml):
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    expected_glm_setup = {
        "sim_name": "GLM Simulation",
        "max_layers": 60,
        "min_layer_vol": 0.0005,
        "min_layer_thick": 0.05,
        "max_layer_thick": 0.1,
        "non_avg": True
    }
    assert my_nml.get_block("glm_setup") == expected_glm_setup

def test_NMLReader_get_block_invalid(ellenbrook_nml):
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    with pytest.raises(TypeError) as error:
        block_name = 123
        setup = my_nml.get_block(block_name)
    assert str(error.value) == (
        f"Expected a string but got type: {type(block_name)}."
    )
    with pytest.raises(ValueError) as error:
        block_name = "foo"
        setup = my_nml.get_block(block_name)
    assert str(error.value) == (
            "Unknown block 'foo'. The following blocks were "
            "read from the NML file: 'glm_setup', 'mixing', 'light', " 
            "'morphometry', 'time', 'output', 'init_profiles', 'meteorology', "
            "'bird_model', 'inflow', 'outflow', 'snowice', 'sediment'."
    )
            
def test_NMLReader_converters_block(ellenbrook_nml):
    converters = {
        "debugging": {
            "disable_evap": nml.NMLReader.read_nml_bool
        }
    }
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    my_nml.set_converters(converters)
    expected_debugging = {
        "disable_evap": False
    }
    debugging = my_nml.get_block("debugging")
    assert debugging == expected_debugging

def test_NMLReader_converters_param(ellenbrook_nml):
    converters = {
        "init_profiles": {
            "foo": nml.NMLReader.read_nml_str,
            "bar": lambda x: nml.NMLReader.read_nml_list(
                x, nml.NMLReader.read_nml_int
            ),
            "num_depths": nml.NMLReader.read_nml_str
        }
    }
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    my_nml.set_converters(converters)
    expected_init_profiles = {
        "lake_depth": 0.15,
        "num_depths": "2",
        "the_depths": [0.01, 0.1],
        "the_temps": [18.0, 10.0],
        "the_sals": [0.5, 1.5],
        "bar": [1, 2, 3],
        "num_wq_vars": 1,
        "foo": "foo",
        "wq_names": [
            "OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"
            ],
        "wq_init_vals": [
            [1.1, 1.2, 1.3, 1.2, 1.3],
            [2.1, 2.2, 2.3, 1.2, 1.3],
            [3.1, 3.2, 3.3, 1.2, 1.3],
            [4.1, 4.2, 4.3, 1.2, 1.3],
            [5.1, 5.2, 5.3, 1.2, 1.3],
            [6.1, 6.2, 6.3, 1.2, 1.3]
        ]
    }
    init_profiles = my_nml.get_block("init_profiles")
    assert init_profiles == expected_init_profiles

def test_NMLReader_get_nml(ellenbrook_nml, ellenbrook_json):
    with open(ellenbrook_json, 'r') as file:
        ellenbrook_dict = json.load(file)
    converters = {
        "init_profiles": {
            "foo": nml.NMLReader.read_nml_str,
            "bar": lambda x: nml.NMLReader.read_nml_list(
                x, nml.NMLReader.read_nml_int
            )
        },
        "debugging": {
            "disable_evap": nml.NMLReader.read_nml_bool
        }
    }
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    my_nml.set_converters(converters)
    my_nml_dict = my_nml.get_nml()
    assert my_nml_dict == ellenbrook_dict

def test_NMLReader_invalid_nml_file():
    nml_file=123
    with pytest.raises(TypeError) as error:
        my_nml = nml.NMLReader(
            nml_file=nml_file
        )
    assert str(error.value) == (
        f"Expected type str or os.PathLike but got {type(nml_file)}."
    )

def test_NMLReader_invalid_json_file(ellenbrook_nml):
    json_file=123
    with pytest.raises(TypeError) as error:
        my_nml = nml.NMLReader(
            nml_file=ellenbrook_nml
        )
        my_nml.write_json(json_file)
    assert str(error.value) == (
        f"Expected type str or os.PathLike but got {type(json_file)}."
    )

def test_NMLReader_json_file(tmp_path, ellenbrook_nml, ellenbrook_json):
    with open(ellenbrook_json, 'r') as file:
        expected_ellenbrook_dict = json.load(file)
    converters = {
        "init_profiles": {
            "foo": nml.NMLReader.read_nml_str,
            "bar": lambda x: nml.NMLReader.read_nml_list(
                x, nml.NMLReader.read_nml_int
            )
        },
        "debugging": {
            "disable_evap": nml.NMLReader.read_nml_bool
        }
    }
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    my_nml.set_converters(converters)
    test_json_file = tmp_path / "test_glm3_nml.json"
    my_nml.write_json(test_json_file)
    with open(test_json_file, 'r') as file:
        test_ellenbrook_dict = json.load(file)
    assert test_ellenbrook_dict == expected_ellenbrook_dict