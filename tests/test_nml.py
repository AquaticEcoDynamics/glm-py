import json
import pytest

from glmpy import nml

def test_nml_bool():
    assert nml.NML.nml_bool(True) == ".true."
    assert nml.NML.nml_bool(False) == ".false."

def test_nml_str():
    python_str = 'temp'
    assert nml.NML.nml_str(python_str) == f"'{python_str}'"

@pytest.mark.parametrize("python_syntax, nml_syntax, syntax_func", [
    ([True], ".true.", nml.NML.nml_bool),
    ([True, False, True], ".true.,.false.,.true.", nml.NML.nml_bool),
    (['temp'], f"'{'temp'}'", nml.NML.nml_str),
    (
        ['temp', 'salt', 'oxy'], 
        f"'{'temp'}','{'salt'}','{'oxy'}'", 
        nml.NML.nml_str
    ),
    ([12.3], "12.3", None),
    ([12.3, 32.4, 64.2], "12.3,32.4,64.2", None)
])

def test_nml_list(python_syntax, nml_syntax, syntax_func):
    assert nml.NML.nml_list(
        python_list=python_syntax,
        syntax_func=syntax_func
    ) == nml_syntax

@pytest.fixture
def example_glmpy_parameters():
    return {
        "param1": True,
        "param2": [True],
        "param3": [True, False, True],
        "param4": 'temp',
        "param5": ['temp'],
        "param6": ['temp', 'salt', 'oxy'],
        "param7": 12.3,
        "param8": [12.3],
        "param9": [12.3, 32.4, 64.2],
        "param10": None,
        "param11": [
            [1.1, 1.2, 1.3, 1.2, 1.3],
            [2.1, 2.2, 2.3, 1.2, 1.3],
            [3.1, 3.2, 3.3, 1.2, 1.3],
            [4.1, 4.2, 4.3, 1.2, 1.3],
            [5.1, 5.2, 5.3, 1.2, 1.3],
            [6.1, 6.2, 6.3, 1.2, 1.3]
        ],
        "param12": [
            [True, True, True, True, True],
            [False, False, False, False, False],
            [False, True, False, True, False]
        ],
        "param13": [
            ["foo", "foo", "foo"],
            ["foo", "foo", "foo"],
            ["foo", "foo", "foo"]
        ]
    }

def test_nml_param_val(example_glmpy_parameters):
    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param1",
        syntax_func=nml.NML.nml_bool
    ) == f"   param1 = .true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param2",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_bool)
    ) == f"   param2 = .true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param3",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_bool)
    ) == f"   param3 = .true.,.false.,.true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param4",
        syntax_func=nml.NML.nml_str
    ) == f"   param4 = 'temp'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param5",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_str)
    ) == f"   param5 = 'temp'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param6",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_str)
    ) == f"   param6 = 'temp','salt','oxy'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param7",
        syntax_func=None
    ) == f"   param7 = 12.3\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param8",
        syntax_func=nml.NML.nml_list
    ) == f"   param8 = 12.3\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param9",
        syntax_func=nml.NML.nml_list
    ) == f"   param9 = 12.3,32.4,64.2\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param10",
        syntax_func=None
    ) == ""

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param11",
        syntax_func=lambda x: nml.NML.nml_array(x, row_indent=13)
    ) == (
        f"   param11 = 1.1,1.2,1.3,1.2,1.3,\n"+
        f"             2.1,2.2,2.3,1.2,1.3,\n"+
        f"             3.1,3.2,3.3,1.2,1.3,\n"+
        f"             4.1,4.2,4.3,1.2,1.3,\n"+
        f"             5.1,5.2,5.3,1.2,1.3,\n"+
        f"             6.1,6.2,6.3,1.2,1.3\n"
    )

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param12",
        syntax_func=lambda x: nml.NML.nml_array(
            x, row_indent=13, syntax_func=nml.NML.nml_bool
        )
    ) == (
        f"   param12 = .true.,.true.,.true.,.true.,.true.,\n"+
        f"             .false.,.false.,.false.,.false.,.false.,\n"+
        f"             .false.,.true.,.false.,.true.,.false.\n"
    )

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param13",
        syntax_func=lambda x: nml.NML.nml_array(
            x, row_indent=13, syntax_func=nml.NML.nml_str
        )
    ) == (
        f"   param13 = 'foo','foo','foo',\n"+
        f"             'foo','foo','foo',\n"+
        f"             'foo','foo','foo'\n"
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
        #"csv_point_frombot": [1], ###
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
    glm_setup = nml.NMLGLMSetup()
    morphometry = nml.NMLMorphometry()
    time = nml.NMLTime()
    init_profiles = nml.NMLInitProfiles()
    mixing = nml.NMLMixing()
    output = nml.NMLOutput()
    meteorology = nml.NMLMeteorology()
    light = nml.NMLLight()
    bird_model = nml.NMLBirdModel()
    inflow = nml.NMLInflow()
    outflow = nml.NMLOutflow()
    sediment = nml.NMLSediment()
    snow_ice = nml.NMLSnowIce()
    wq_setup = nml.NMLWQSetup()

    glm_setup.set_attributes(example_glm_setup_parameters)
    morphometry.set_attributes(example_morphometry_parameters)
    time.set_attributes(example_time_parameters)
    init_profiles.set_attributes(example_init_profiles_parameters)
    mixing.set_attributes(example_mixing_parameters)
    output.set_attributes(example_output_parameters)
    meteorology.set_attributes(example_meteorology_parameters)
    light.set_attributes(example_light_parameters)
    bird_model.set_attributes(example_bird_model_parameters)
    inflow.set_attributes(example_inflow_parameters)
    outflow.set_attributes(example_outflow_parameters)
    sediment.set_attributes(example_sediment_parameters)
    snow_ice.set_attributes(example_snow_ice_parameters)
    wq_setup.set_attributes(example_wq_setup_parameters)

    nml_file = nml.NML(
        glm_setup=glm_setup(),
        morphometry=morphometry(),
        time=time(),
        init_profiles=init_profiles(),
        mixing=mixing(),
        output=output(),
        meteorology=meteorology(),
        light=light(),
        bird_model=bird_model(),
        inflow=inflow(),
        outflow=outflow(),
        sediment=sediment(),
        snow_ice=snow_ice(),
        wq_setup=wq_setup(),
        check_errors=False
    )
    file_path = tmp_path / "test.nml"
    nml_file.write_nml(file_path)

    with open(file_path, "r") as file:
        content = file.read()
    
    expected = (
        "&glm_setup\n" +
        f"   sim_name = 'Example Simulation #1'\n" +
        f"   max_layers = 500\n" +
        f"   min_layer_vol = 0.025\n" +
        f"   min_layer_thick = 0.15\n" +
        f"   max_layer_thick = 1.5\n" +
        f"   density_model = 1\n" +
        f"   non_avg = .false.\n" +
        "/" + 
        "\n" +
        "&mixing\n" +
        f"   surface_mixing = 1\n" +
        f"   coef_mix_conv = 0.125\n" +
        f"   coef_wind_stir = 0.23\n" +
        f"   coef_mix_shear = 0.2\n" +
        f"   coef_mix_turb = 0.51\n" +
        f"   coef_mix_KH = 0.3\n" +
        f"   deep_mixing = 2\n" +
        f"   coef_mix_hyp = 0.5\n" +
        f"   diff = 0.0\n" +
        "/" +
        "\n" +
        "&morphometry\n" +
        f"   lake_name = 'Example Lake'\n" +
        f"   latitude = 32.0\n" +
        f"   longitude = 35.0\n" +
        f"   base_elev = -252.9\n" +
        f"   crest_elev = -203.9\n" +
        f"   bsn_len = 21000.0\n" +
        f"   bsn_wid = 13000.0\n" +
        f"   bsn_vals = 45\n" +
        f"   H = -252.9,-251.9,-250.9,-249.9,-248.9,-247.9,-246.9,-245.9," +
        "-244.9,-243.9,-242.9,-241.9,-240.9,-239.9,-238.9,-237.9," +
        "-236.9,-235.9,-234.9,-233.9,-232.9,-231.9,-230.9,-229.9," + 
        "-228.9,-227.9,-226.9,-225.9,-224.9,-223.9,-222.9,-221.9," + 
        "-220.9,-219.9,-218.9,-217.9,-216.9,-215.9,-214.9,-213.9," + 
        "-212.9,-211.9,-208.9,-207.9,-203.9\n"
        f"   A = 0,9250000,15200000,17875000,21975000,26625000,31700000," +
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
        f"   timefmt = 3\n" +
        f"   start = '1997-01-01 00:00:00'\n" +
        f"   stop = '1999-01-01 00:00:00'\n" +
        f"   dt = 3600.0\n" +
        f"   num_days = 730\n" +
        f"   timezone = 7.0\n" +
        "/" +
        "\n" +
        "&output\n" +
        f"   out_dir = 'output'\n" +
        f"   out_fn = 'output'\n" +
        f"   nsave = 6\n" +
        f"   csv_lake_fname = 'lake'\n" +
        f"   csv_point_nlevs = 2\n" +
        f"   csv_point_fname = 'WQ_'\n" +
        f"   csv_point_at = 5,30\n" +
        f"   csv_point_nvars = 7\n" +
        f"   csv_point_vars = 'temp','salt','OXY_oxy','SIL_rsi','NIT_amm'," +
        "'NIT_nit','PHS_frp'\n" +
        f"   csv_outlet_allinone = .false.\n" +
        f"   csv_outlet_fname = 'outlet_'\n" +
        f"   csv_outlet_nvars = 4\n" +
        f"   csv_outlet_vars = 'flow','temp','salt','OXY_oxy'\n" +
        f"   csv_ovrflw_fname = 'overflow'\n" + 
        "/" + 
        "\n"+
        "&init_profiles\n" +
        f"   lake_depth = 43\n" +
        f"   num_depths = 3\n" +
        f"   the_depths = 1,20,40\n" +
        f"   the_temps = 18.0,18.0,18.0\n" +
        f"   the_sals = 0.5,0.5,0.5\n" +
        f"   num_wq_vars = 6\n" +
        f"   wq_names = 'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc'," +
        "'OGM_poc'\n" +
        f"   wq_init_vals = 1.1,1.2,1.3,1.2,1.3,\n" +
        "                  2.1,2.2,2.3,1.2,1.3,\n" +
        "                  3.1,3.2,3.3,1.2,1.3,\n" +
        "                  4.1,4.2,4.3,1.2,1.3,\n" +
        "                  5.1,5.2,5.3,1.2,1.3,\n" +
        "                  6.1,6.2,6.3,1.2,1.3\n" +
        "/" +
        "\n" +
        "&meteorology\n" +
        f"   met_sw = .true.\n" +
        f"   meteo_fl = 'bcs/met_hourly.csv'\n" +
        f"   subdaily = .true.\n" +
        f"   rad_mode = 1\n" +
        f"   albedo_mode = 1\n" +
        f"   lw_type = 'LW_IN'\n" +
        f"   cloud_mode = 4\n" +
        f"   atm_stab = 0\n" +
        f"   ce = 0.0013\n" +
        f"   ch = 0.0013\n" +
        f"   rain_sw = .false.\n" +
        f"   catchrain = .true.\n" +
        f"   rain_threshold = 0.001\n" +
        f"   runoff_coef = 0.0\n" +
        f"   cd = 0.0013\n" +
        f"   wind_factor = 0.9\n" +
        f"   fetch_mode = 0\n" +
        "/" +
        "\n" +
        "&light\n" +
        f"   light_mode = 0\n" +
        f"   Kw = 0.4\n" +
        f"   n_bands = 4\n" +
        f"   light_extc = 1.0,0.5,2.0,4.0\n" +
        f"   energy_frac = 0.51,0.45,0.035,0.005\n" +
        f"   Benthic_Imin = 10\n" +
        "/" +
        "\n" +
        "&bird_model\n" +
        f"   AP = 973\n" +
        f"   Oz = 0.279\n" +
        f"   WatVap = 1.1\n" +
        f"   AOD500 = 0.033\n" +
        f"   AOD380 = 0.038\n" +
        f"   Albedo = 0.2\n" +
        "/" +
        "\n" +
        "&inflow\n" +
        f"   num_inflows = 6\n" +
        f"   names_of_strms = 'Inflow1','Inflow2','Inflow3','Inflow4',"+
        "'Inflow5','Inflow6'\n" +
        f"   subm_flag = .false.,.false.,.false.,.true.,.false.,.false.\n" +
        f"   strm_hf_angle = 85.0,85.0,85.0,85.0,85.0,85.0\n" +
        f"   strmbd_slope = 4.0,4.0,4.0,4.0,4.0,4.0\n" +
        f"   strmbd_drag = 0.016,0.016,0.016,0.016,0.016,0.016\n" +
        f"   coef_inf_entrain = 0.0\n" +
        f"   inflow_factor = 1.0,1.0,1.0,1.0,1.0,1.0\n" +
        f"   inflow_fl = 'bcs/inflow_1.csv','bcs/inflow_2.csv'," +
        "'bcs/inflow_3.csv','bcs/inflow_4.csv','bcs/inflow_5.csv'," + 
        "'bcs/inflow_6.csv'\n" +
        f"   inflow_varnum = 3\n" +
        f"   inflow_vars = 'FLOW','TEMP','SALT'\n" +
        f"   time_fmt = 'YYYY-MM-DD hh:mm:ss'\n" +
        "/" +
        "\n" +
        "&outflow\n" +
        f"   num_outlet = 1\n" +
        f"   outflow_fl = 'bcs/outflow.csv'\n" +
        f"   outflow_factor = 1.0\n" +
        f"   flt_off_sw = .false.\n" +
        f"   outlet_type = 1\n" +
        f"   outl_elvs = -215.5\n" +
        f"   bsn_len_outl = 18000\n" +
        f"   bsn_wid_outl = 11000\n" +
        f"   seepage = .true.\n" +
        f"   seepage_rate = 0.01\n" +
        "/" +
        "\n" +
        "&sediment\n" +
        f"   sed_heat_Ksoil = 0.0\n" +
        f"   sed_temp_depth = 0.2\n" +
        f"   sed_temp_mean = 5,10,20\n" +
        f"   sed_temp_amplitude = 6,8,10\n" +
        f"   sed_temp_peak_doy = 80,70,60\n" +
        f"   benthic_mode = 1\n" +
        f"   n_zones = 3\n" +
        f"   zone_heights = 10.0,20.0,50.0\n" +
        f"   sed_reflectivity = 0.1,0.01,0.01\n" +
        f"   sed_roughness = 0.1,0.01,0.01\n" +
        "/" +
        "\n" +
        "&snowice\n" +
        f"   snow_albedo_factor = 1.0\n" +
        f"   snow_rho_min = 50\n" +
        f"   snow_rho_max = 300\n" +
        "/" +
        "\n" +
        "&wq_setup\n" +
        f"   wq_lib = 'aed2'\n" +
        f"   wq_nml_file = 'aed2/aed2.nml'\n" +
        f"   bioshade_feedback = .true.\n" +
        f"   mobility_off = .false.\n" +
        f"   ode_method = 1\n" +
        f"   split_factor = 1\n" +
        f"   repair_state = .true.\n" +
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
    ) == True
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_2"]
    ) == False
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_3"]
    ) == True
    assert nml.NMLReader.read_nml_bool(
        nml_bool=example_nml_parameters["nml_bool_4"]
    ) == False

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
        syntax_func=nml.NMLReader.read_nml_str
    ) == ["foo", "bar", "baz"]
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_2"],
        syntax_func=nml.NMLReader.read_nml_int
    ) == [1, 2, 3]
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_3"],
        syntax_func=nml.NMLReader.read_nml_float
    ) == [1.1, 2.1, 3.1]
    assert nml.NMLReader.read_nml_list(
        nml_list=example_nml_parameters["nml_list_4"],
        syntax_func=nml.NMLReader.read_nml_bool
    ) == [True, False, True, False]

    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_1"],
        syntax_func=nml.NMLReader.read_nml_int
    ) == [[1, 2, 3], [4, 5, 6]]
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_2"],
        syntax_func=nml.NMLReader.read_nml_float
    ) == [[1.1, 2.1, 3.1], [1.2, 2.2, 3.2]] 
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_3"],
        syntax_func=nml.NMLReader.read_nml_str
    ) == [['foo', 'bar', 'baz'], ["foo", "bar", "baz"]]
    assert nml.NMLReader.read_nml_array(
        nml_array=example_nml_parameters["nml_array_4"],
        syntax_func=nml.NMLReader.read_nml_bool
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
        syntax_func = "foo"
        nml.NMLReader.read_nml_list(input, syntax_func)
    assert str(error.value) == (
        f"Expected a Callable but got type: {type(syntax_func)}."
    )
    with pytest.raises(TypeError) as error:
        input = ["foo, baz, bar", 123]
        syntax_func = nml.NMLReader.read_nml_str
        nml.NMLReader.read_nml_list(input, syntax_func)
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
        syntax_func = "foo"
        nml.NMLReader.read_nml_array(input, syntax_func)
    assert str(error.value) == (
        f"Expected a Callable but got type: {type(syntax_func)}."
    )
    with pytest.raises(TypeError) as error:
        input = ["1.1, 1.2, 1.3", 123]
        syntax_func = nml.NMLReader.read_nml_float
        nml.NMLReader.read_nml_array(input, syntax_func)
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
            f"Unknown block 'foo'. The following blocks were "
            "read from the NML file: 'glm_setup', 'mixing', 'light', " 
            "'morphometry', 'time', 'output', 'init_profiles', 'meteorology', "
            "'bird_model', 'inflow', 'outflow', 'snowice', 'sediment'."
    )
            
def test_NMLReader_type_mappings_block(ellenbrook_nml):
    type_mappings = {
        "debugging": {
            "disable_evap": nml.NMLReader.read_nml_bool
        }
    }
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    my_nml.set_type_mappings(type_mappings)
    expected_debugging = {
        "disable_evap": False
    }
    debugging = my_nml.get_block("debugging")
    assert debugging == expected_debugging

def test_NMLReader_type_mappings_param(ellenbrook_nml):
    type_mappings = {
        "init_profiles": {
            "foo": nml.NMLReader.read_nml_str,
            "bar": lambda x: nml.NMLReader.read_nml_list(
                x, nml.NMLReader.read_nml_int
            ),
            "num_depths": nml.NMLReader.read_nml_str
        }
    }
    my_nml = nml.NMLReader(nml_file=ellenbrook_nml)
    my_nml.set_type_mappings(type_mappings)
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
    type_mappings = {
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
    my_nml.set_type_mappings(type_mappings)
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
    type_mappings = {
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
    my_nml.set_type_mappings(type_mappings)
    test_json_file = tmp_path / "test_glm3_nml.json"
    my_nml.write_json(test_json_file)
    with open(test_json_file, 'r') as file:
        test_ellenbrook_dict = json.load(file)
    assert test_ellenbrook_dict == expected_ellenbrook_dict